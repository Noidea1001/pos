# sales/views.py
from django.db.models import DecimalField
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import OrderForm, OrderDetailFormSet
from .models import Order


@login_required
def order_list(request):
    orders = (
        Order.objects.select_related("customer", "user")
        .prefetch_related("items__product")
    )
    return render(request, "sales/order_list.html", {"orders": orders})


@login_required
@transaction.atomic
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            formset.instance = order

            details = formset.save(commit=False)
            for detail in details:
                product = Product.objects.select_for_update().get(pk=detail.product_id)
                if product.stock < detail.quantity:
                    form.add_error(None, f"Insufficient stock for {product.name}")
                    transaction.set_rollback(True)
                    return render(
                        request,
                        "sales/order_form.html",
                        {"form": form, "formset": formset},
                    )
                Product.objects.filter(pk=product.pk).update(
                    stock=F("stock") - detail.quantity
                )
                detail.save()
            for obj in formset.deleted_objects:
                obj.delete()

            order.recalculate()
            order.save(update_fields=["total_amount", "total_remain"])
            return redirect("order_detail", pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderDetailFormSet()
    return render(request, "sales/order_form.html", {"form": form, "formset": formset})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer", "user").prefetch_related("items__product"),
        pk=pk,
    )
    return render(request, "sales/order_detail.html", {"order": order})


@login_required
@permission_required("sales.delete_order", raise_exception=True)
@transaction.atomic
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        for item in order.items.select_related("product"):
            Product.objects.filter(pk=item.product_id).update(
                stock=F("stock") + item.quantity
            )
        order.delete()
        return redirect("order_list")
    return render(request, "sales/order_confirm_delete.html", {"order": order})

@login_required
def order_report(request):
    qs = Order.objects.select_related("customer", "user")

    customer_id = request.GET.get("customer")
    user_id = request.GET.get("user")
    date_from = parse_date(request.GET.get("from", "") or "")
    date_to = parse_date(request.GET.get("to", "") or "")

    if customer_id:
        qs = qs.filter(customer_id=customer_id)
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
    return render(request, "sales/order_report.html", {"orders": qs, "totals": totals})