from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .models import Note

class NoteListView(ListView):
    model = Note
    template_name = "Notes_app/list.html"
    context_object_name = "notes"
    
class NoteDeleteView(DeleteView):
    model = Note
    template_name = "Notes_app/delete.html"
    success_url = reverse_lazy('note-list') 

class NoteCreateView(CreateView):
    model = Note
    template_name = "Notes_app/create.html"
    fields = ['title', 'content']
    success_url = reverse_lazy('note-list') 

class NoteUpdateView(UpdateView):   
    model =Note
    template_name = "Notes_app/update.html" 
    fields = ['title', 'content']
    success_url = reverse_lazy('note-list') 
