from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

# from django.db import models
# from django.contrib.auth.models import User
# class Note(models.Model):

#     # ───── choice lists ──────────────────────────
#     CATEGORY_CHOICES = [
#         ("work", "Work"),
#         ("personal", "Personal"),
#         ("urgent", "Urgent"),
#         ("other", "Other"),
#     ]
#     PRIORITY_CHOICES = [
#         ("low", "Low"),
#         ("medium", "Medium"),
#         ("high", "High"),
#     ]

#     # ───── fields ────────────────────────
#     name        = models.CharField(max_length=100)
#     description = models.TextField()
#     color       = models.CharField(max_length=20, blank=True, null=True)   
#     created_at  = models.DateTimeField(auto_now_add=True)
#     is_active   = models.BooleanField(default=True)
#     start_date  = models.DateField(blank=True, null=True)
#     end_date    = models.DateField(blank=True, null=True)
#     start_time  = models.TimeField(blank=True, null=True)
#     end_time    = models.TimeField(blank=True, null=True)
#     created_by  = models.ForeignKey(User, on_delete=models.SET_NULL,
#                                     blank=True, null=True,
#                                     related_name="notes")
#     email       = models.EmailField()
#     priority    = models.CharField(max_length=10,
#                                    choices=PRIORITY_CHOICES,
#                                    default="low")
#     category    = models.CharField(max_length=20,
#                                    choices=CATEGORY_CHOICES,
#                                    default="other")
#     notes       = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name
