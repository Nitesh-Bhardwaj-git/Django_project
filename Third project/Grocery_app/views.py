from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import GroceryItem
from .forms import GroceryItemForm


class ItemList(ListView):
    model = GroceryItem
    template_name = "Grocery_app/list.html"
    context_object_name = "items"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return GroceryItem.objects.filter(created_by=self.request.user)
        return GroceryItem.objects.none()



class ItemCreate(CreateView):
    model = GroceryItem
    form_class = GroceryItemForm
    template_name = "Grocery_app/create.html"
    success_url = reverse_lazy("item-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



   


class ItemUpdate(UpdateView):
    model = GroceryItem
    form_class = GroceryItemForm
    template_name = "Grocery_app/update.html"
    success_url = reverse_lazy("item-list")


class ItemDelete(DeleteView):
    model = GroceryItem
    template_name = "Grocery_app/delete.html"
    success_url = reverse_lazy("item-list")
