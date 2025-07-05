from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import Todo
from django.urls import reverse_lazy

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "Todo/list.html"
    context_object_name = "todos"
    login_url = 'login'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model =Todo
    template_name = "Todo/update.html"
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo-list')   

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = "Todo/delete.html"
    success_url = reverse_lazy('todo-list') 

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = "Todo/create.html"
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = "Todo/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

class RegisterView(CreateView):
    template_name = "Todo/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class DashboardView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "Todo/dashboard.html"
    context_object_name = "todos"
    login_url = 'login'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todos = self.get_queryset()
        context['total_todos'] = todos.count()
        context['completed_todos'] = todos.filter(completed=True).count()
        context['pending_todos'] = todos.filter(completed=False).count()
        return context

