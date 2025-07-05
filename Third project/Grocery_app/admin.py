from django.contrib import admin
from .models import GroceryItem

@admin.register(GroceryItem)
class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "quantity", "unit",
                    "category", "total_price", "is_purchased")
    list_filter  = ("category", "is_purchased", "store_name")
    search_fields = ("item_name", "store_name", "email")
