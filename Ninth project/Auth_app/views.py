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
    template_name = "Auth_app/list.html"
    context_object_name = "todos"
    login_url = 'login'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model =Todo
    template_name = "Auth_app/update.html"
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo-list')   

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = "Auth_app/delete.html"
    success_url = reverse_lazy('todo-list') 

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = "Auth_app/create.html"
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = "Auth_app/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

class RegisterView(CreateView):
    template_name = "Auth_app/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

class DashboardView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "Auth_app/dashboard.html"
    context_object_name = "auths"
    login_url = 'login'

    

