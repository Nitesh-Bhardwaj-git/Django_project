from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class DashboardView(TemplateView):
    template_name = "dashboard.html"

class LoginView(AuthLoginView):
    template_name = "login.html"
    
    def get_success_url(self):
        messages.success(self.request, 'Login successful!')
        return reverse_lazy('dashboard')

class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logout successful!')
        return super().dispatch(request, *args, **kwargs)
