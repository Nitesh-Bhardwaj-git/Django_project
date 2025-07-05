from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Book(models.Model):
    title  = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    category = models.CharField(max_length=150, blank=True, null=True)
    publication_year = models.CharField(blank=True, null=True)
    copies_total     = models.CharField(default=3)
    copies_available = models.CharField(default=3)

    def __str__(self):
        return f"{self.title} by {self.author}"



class Member(models.Model):
    name    = models.CharField(max_length=255)
    email   = models.EmailField(unique=True)
    phone   = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    STATUS_CHOICES = [("borrowed", "Borrowed"), ("returned", "Returned")]

    book        = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    member      = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    loan_date   = models.DateField(default=timezone.now)
    due_date    = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default="borrowed")


    def __str__(self):
        return f"{self.book} → {self.member}"


class Fine(models.Model):
    loan   = models.OneToOneField(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid   = models.BooleanField(default=False)

    def __str__(self):
        if self.loan:
            return f"{self.amount} for {self.loan}"
        else:
            return f"{self.amount} for {self.member}"

