# from django.db import models

# # Create your models here.
# class Grocery(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField()
#     description = models.TextField(blank=True, null=True)

    

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class GroceryItem(models.Model):
    # ---------- field choices ----------
    UNIT_CHOICES = [
        ('kg',  'kg'),
        ('g',   'g'),
        ('l',   'l'),
        ('ml',  'ml'),
        ('pcs', 'pcs'),
    ]
    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits',     'Fruits'),
        ('dairy',      'Dairy'),
        ('bakery',     'Bakery'),
        ('meat',       'Meat'),
        ('snacks',     'Snacks'),
        ('beverages',  'Beverages'),
        ('other',      'Other'),
    ]

    # ---------- core columns ----------
    item_name      = models.CharField(max_length=100)
    quantity       = models.DecimalField(max_digits=8, decimal_places=2,
                                         validators=[MinValueValidator(0.01)])
    unit           = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2,
                                         validators=[MinValueValidator(0)])
    total_price    = models.DecimalField(max_digits=10, decimal_places=2,
                                         editable=False)
    is_purchased   = models.BooleanField(default=False)
    purchase_date  = models.DateField(blank=True, null=True)
    expiry_date    = models.DateField(blank=True, null=True)
    store_name     = models.CharField(max_length=100, blank=True)
    created_by     = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="grocery_items"
    )
    email          = models.EmailField()
    category       = models.CharField(max_length=20,
                                      choices=CATEGORY_CHOICES,
                                      default='other')

    created_at     = models.DateTimeField(auto_now_add=True)

    # ---------- helpers ----------
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item_name} – {self.quantity}{self.unit}"
