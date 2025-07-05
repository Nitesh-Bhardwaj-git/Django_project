from django.db import models
from django.contrib.auth.models import User as user

# Create your models here.
class Todo(models.Model):
    user=models.ForeignKey(user, on_delete=models.CASCADE, null=True)    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)