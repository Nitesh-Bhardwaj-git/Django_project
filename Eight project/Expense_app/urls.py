# expenses/urls.py
from django.urls import path
from .views import (ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView, DashboardView, RegisterView)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("list/",            ExpenseListView.as_view(), name="expense_list"),
    path("add/",             ExpenseCreateView.as_view(),   name="expense_add"),
    path("<int:pk>/update/", ExpenseUpdateView.as_view(),   name="expense_update"),
    path("<int:pk>/delete/", ExpenseDeleteView.as_view(),   name="expense_delete"),
    path("register/", RegisterView.as_view(), name="register"),
]
