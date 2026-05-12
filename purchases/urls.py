# purchases/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.purchase_list, name="purchase_list"),
    path("add/", views.purchase_create, name="purchase_create"),
    path("<int:pk>/", views.purchase_detail, name="purchase_detail"),
    path("<int:pk>/delete/", views.purchase_delete, name="purchase_delete"),
    path("report/", views.purchase_report, name="purchase_report"),
]