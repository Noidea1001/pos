# sales/forms.py
from django import forms
from django.forms import inlineformset_factory

from .models import Order, OrderDetail


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "total_paid"]


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ["product", "quantity"]


OrderDetailFormSet = inlineformset_factory(
    Order,
    OrderDetail,
    form=OrderDetailForm,
    extra=3,
    can_delete=True,
)