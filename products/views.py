# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from .forms import CategoryForm, ProductForm
from django.contrib.auth.decorators import login_required

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "products/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "products/category_form.html", {"form": form})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "products/category_form.html", {"form": form})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(
        request,
        "products/category_confirm_delete.html",
        {"category": category},
    )


@login_required
def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "products/product_list.html", {"products": products})


@login_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "products/product_form.html", {"form": form})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(request, "products/product_detail.html", {"product": product})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "products/product_form.html", {"form": form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(
        request,
        "products/product_confirm_delete.html",
        {"product": product},
    )