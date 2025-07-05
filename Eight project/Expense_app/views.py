from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView)
from .models import Expense
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "Expense_app/list.html"
    context_object_name = "expenses"
    ordering = ["-date"]                    


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ["name", "amount", "date"]
    template_name = "Expense_app/create.html"
    success_url = reverse_lazy("expense_list")


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ["name", "amount", "date"]
    template_name = "Expense_app/update.html"
    success_url = reverse_lazy("expense_list")


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = "Expense_app/delete.html"
    success_url = reverse_lazy("expense_list")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "Expense_app/dashboard.html"


class RegisterView(CreateView):
    template_name = "Expense_app/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    redirect_authenticated_user = True
    