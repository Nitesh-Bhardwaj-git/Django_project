from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from collections import defaultdict
from decimal import Decimal


def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    total_income = sum(t.amount for t in expenses if t.type == 'income')
    total_expense = sum(t.amount for t in expenses if t.type == 'expense')
    balance = total_income - total_expense
    # Category breakdown (for expenses only)
    category_totals = defaultdict(lambda: Decimal('0.0'))
    for t in expenses.filter(type='expense'):
        category_totals[t.category] += t.amount
    return render(request, 'Expense_app/list.html', {
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_totals': dict(category_totals),
    })


def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.type = 'expense'
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'Expense_app/create.html', {'form': form, 'is_income': False})


def expense_income_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.type = 'income'
            income.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'Expense_app/create.html', {'form': form, 'is_income': True})


def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'Expense_app/update.html', {'form': form, 'expense': expense})


def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'Expense_app/delete.html', {'expense': expense})



    