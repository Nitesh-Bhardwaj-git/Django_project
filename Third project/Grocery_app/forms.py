from django import forms
from .models import GroceryItem

class GroceryItemForm(forms.ModelForm):
    class Meta:
        model  = GroceryItem
        exclude = ("created_by", "total_price")   # handled automatically
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "expiry_date":   forms.DateInput(attrs={"type": "date"}),
        }
