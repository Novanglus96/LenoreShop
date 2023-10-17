from django.contrib import admin
from .models import Store, Aisle, Item, ShoppingList, ListItem

# Register your models here.

admin.site.register(Store)
admin.site.register(Aisle)
admin.site.register(Item)
admin.site.register(ShoppingList)
admin.site.register(ListItem)