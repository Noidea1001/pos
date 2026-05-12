# sales/admin.py
from django.contrib import admin
from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "user", "total_amount", "total_paid", "total_remain", "created_at")
    inlines = [OrderDetailInline]