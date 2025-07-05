from django.db import models
from django.utils import timezone

class Expense(models.Model):
    name   = models.CharField(max_length=200)                 
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    date   = models.DateField(default=timezone.now) 
