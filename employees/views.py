# employees/views.py
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmployeeCreateForm, EmployeeUpdateForm, ProfileForm

User = get_user_model()

@login_required
def employee_list(request):
    employees = User.objects.select_related("profile").order_by("username")
    return render(request, "employees/employee_list.html", {"employees": employees})

@login_required
def employee_create(request):
    form = EmployeeCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        profile_form.instance = user.profile
        profile_form.save()
        return redirect("employee_list")
    return render(
        request,
        "employees/employee_form.html",
        {"form": form, "profile_form": profile_form},
    )

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(User.objects.select_related("profile"), pk=pk)
    return render(request, "employees/employee_detail.html", {"employee": employee})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(User, pk=pk)
    form = EmployeeUpdateForm(request.POST or None, instance=employee)
    profile_form = ProfileForm(request.POST or None, instance=employee.profile)
    if form.is_valid() and profile_form.is_valid():
        form.save()
        profile_form.save()
        return redirect("employee_list")
    return render(
        request,
        "employees/employee_form.html",
        {"form": form, "profile_form": profile_form},
    )

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        employee.is_active = False
        employee.save(update_fields=["is_active"])
        return redirect("employee_list")
    return render(
        request,
        "employees/employee_confirm_delete.html",
        {"employee": employee},
    )
