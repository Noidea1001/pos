# dashboard/views.py
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render
from customers.models import Customer
from suppliers.models import Supplier
from products.models import Product, Category
from sales.models import Order
from purchases.models import Purchase


@login_required
def dashboard_home(request):
    zero = Coalesce(Sum("total_amount"), Decimal("0"), output_field=DecimalField())
    context = {
        "total_categories": Category.objects.aggregate(n=Count("id"))["n"],
        "total_products": Product.objects.aggregate(n=Count("id"))["n"],
        "total_customers": Customer.objects.aggregate(n=Count("id"))["n"],
        "total_suppliers": Supplier.objects.aggregate(n=Count("id"))["n"],
        "order_count": Order.objects.aggregate(n=Count("id"))["n"],
        "purchase_count": Purchase.objects.aggregate(n=Count("id"))["n"],
        "total_order_amount": Order.objects.aggregate(t=zero)["t"],
        "total_purchase_amount": Purchase.objects.aggregate(t=zero)["t"],
    }
    return render(request, "dashboard/home.html", context)