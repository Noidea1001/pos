# sales/models.py
from decimal import Decimal
from django.conf import settings
from django.db import models

from customers.models import Customer
from products.models import Product


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    total_remain = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.customer.name}"

    def recalculate(self) -> None:
        total = sum((item.total_price for item in self.items.all()), Decimal("0"))
        self.total_amount = total
        self.total_remain = total - self.total_paid


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))

    def save(self, *args, **kwargs) -> None:
        self.total_price = self.product.selling_price * self.quantity
        super().save(*args, **kwargs)
