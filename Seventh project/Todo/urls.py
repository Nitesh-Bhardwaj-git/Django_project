from django.urls import path
from.views import TodoListView, TodoUpdateView, TodoDeleteView, TodoCreateView, CustomLoginView, RegisterView, DashboardView

urlpatterns=[
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('todos/', TodoListView.as_view(), name='todo-list'),
    path('update/<int:pk>/', TodoUpdateView.as_view(), name='todo-update'),
    path('delete/<int:pk>/', TodoDeleteView.as_view(), name='todo-delete'),
    path('create/', TodoCreateView.as_view(), name='todo-create'),
]