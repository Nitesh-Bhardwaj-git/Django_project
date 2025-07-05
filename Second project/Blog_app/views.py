from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Create your views here.
from .models import Blog

class BlogListView(ListView):
    model = Blog
    template_name = "Blog_app/list.html"
    context_object_name = "blogs"

class BlogCreateView(CreateView):
    model = Blog
    template_name = "Blog_app/create.html"
    fields = ['title', 'content', 'author']
    success_url = reverse_lazy('blog-list')  

class BlogUpdateView(UpdateView):
    model = Blog
    template_name = "Blog_app/update.html"
    fields = ['title', 'content', 'author']
    success_url = reverse_lazy('blog-list')

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "Blog_app/delete.html"
    success_url = reverse_lazy('blog-list')  
    
    