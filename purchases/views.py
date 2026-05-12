# purchases/views.py
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import PurchaseForm, PurchaseDetailFormSet
from .models import Purchase
from decimal import Decimal
from django.db.models import Sum, DecimalField
from django.utils.dateparse import parse_date
from django.db.models.functions import Coalesce

@login_required
def purchase_list(request):
    purchases = (
        Purchase.objects.select_related("supplier", "user")
        .prefetch_related("items__product")
    )
    return render(request, "purchases/purchase_list.html", {"purchases": purchases})


@login_required
@transaction.atomic
def purchase_create(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        formset = PurchaseDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()
            formset.instance = purchase

            details = formset.save(commit=False)
            for detail in details:
                detail.save()
                Product.objects.filter(pk=detail.product_id).update(
                    stock=F("stock") + detail.quantity
                )
            for obj in formset.deleted_objects:
                obj.delete()

            purchase.recalculate()
            purchase.save(update_fields=["total_amount", "total_remain"])
            return redirect("purchase_detail", pk=purchase.pk)
    else:
        form = PurchaseForm()
        formset = PurchaseDetailFormSet()
    return render(
        request,
        "purchases/purchase_form.html",
        {"form": form, "formset": formset},
    )


@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(
        Purchase.objects.select_related("supplier", "user").prefetch_related("items__product"),
        pk=pk,
    )
    return render(request, "purchases/purchase_detail.html", {"purchase": purchase})


@login_required
@transaction.atomic
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == "POST":
        for item in purchase.items.select_related("product"):
            Product.objects.filter(pk=item.product_id).update(
                stock=F("stock") - item.quantity
            )
        purchase.delete()
        return redirect("purchase_list")
    return render(
        request,
        "purchases/purchase_confirm_delete.html",
        {"purchase": purchase},
    )
@login_required
def purchase_report(request):
    qs = Purchase.objects.select_related("supplier", "user")

    supplier_id = request.GET.get("supplier")
    user_id = request.GET.get("user")
    date_from = parse_date(request.GET.get("from", "") or "")
    date_to = parse_date(request.GET.get("to", "") or "")

    if supplier_id:
        qs = qs.filter(supplier_id=supplier_id)
    if user_id:
        qs = qs.filter(user_id=user_id)
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    totals = qs.aggregate(
        total_amount=Coalesce(Sum("total_amount"), Decimal("0"), output_field=DecimalField()),
        total_paid=Coalesce(Sum("total_paid"), Decimal("0"), output_field=DecimalField()),
        total_remain=Coalesce(Sum("total_remain"), Decimal("0"), output_field=DecimalField()),
    )
    return render(
        request,
        "purchases/purchase_report.html",
        {"purchases": qs, "totals": totals},
    )