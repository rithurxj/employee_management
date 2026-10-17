from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Employee
from .forms import EmployeeForm


def home(request):
    search = request.GET.get('search', '')

    employees = Employee.objects.all()

    if search:
        employees = employees.filter(
            Q(name__icontains=search) |
            Q(department__icontains=search)
        )

    total = employees.count()

    return render(request, 'employees/home.html', {
        'employees': employees,
        'total': total,
        'search': search,
    })


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()

    return render(request, 'employees/add.html', {
        'form': form
    })


def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        employee.delete()

    return redirect('home')


def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/edit.html', {
        'form': form
    })