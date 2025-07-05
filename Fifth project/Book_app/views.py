from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book, Member, Loan, Fine



class BookList(ListView):
    model = Book
    template_name = "Book_app/list.html"
    context_object_name = "books"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.all()
        context['loans'] = Loan.objects.all()
        context['fines'] = Fine.objects.all()
        return context


class MemberList(ListView):
    model = Member
    template_name = "Book_app/list.html"
    context_object_name = "members"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['loans'] = Loan.objects.all()
        context['fines'] = Fine.objects.all()
        return context


class LoanList(ListView):
    model = Loan
    template_name = "Book_app/list.html"
    context_object_name = "loans"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['members'] = Member.objects.all()
        context['fines'] = Fine.objects.all()
        return context


class FineList(ListView):
    model = Fine
    template_name = "Book_app/list.html"
    context_object_name = "fines"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['members'] = Member.objects.all()
        context['loans'] = Loan.objects.all()
        return context


class MemberCreate(CreateView):
    model = Member
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("member-list")


class BookCreate(CreateView):
    model = Book
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("book-list")


class LoanCreate(CreateView):
    model = Loan
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("loan-list")


class FineCreate(CreateView):
    model = Fine
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("fine-list")


class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("book-list")


class MemberUpdate(UpdateView):
    model = Member
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("member-list")


class LoanUpdate(UpdateView):
    model = Loan
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("loan-list")


class FineUpdate(UpdateView):
    model = Fine
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("fine-list")


class BookDelete(DeleteView):
    model = Book
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("book-list")


class MemberDelete(DeleteView):
    model = Member
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("member-list")


class LoanDelete(DeleteView):
    model = Loan
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("loan-list")


class FineDelete(DeleteView):
    model = Fine
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("fine-list")
