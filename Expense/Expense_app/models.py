from django.db import models
from django.utils import timezone

class Expense(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    name   = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date   = models.DateField(default=timezone.now)
    type   = models.CharField(max_length=7, choices=TYPE_CHOICES, default='expense')
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"