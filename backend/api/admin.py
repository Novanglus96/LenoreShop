from django.contrib import admin
from .models import Store, Aisle, Item, ShoppingList, ListItem, Version

# Register your models here.


class StoreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    search_fields = ["name"]

    ordering = ["name"]


class AisleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "order", "store"]

    list_filter = ["store"]

    ordering = ["store", "order", "name"]


class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "matches", "plural", "aisle"]

    list_filter = ["aisle"]

    ordering = ["name"]


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ["id", "store", "name"]

    list_filter = ["store"]

    ordering = ["store", "name"]


class ListItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "shopping_list",
        "aisle",
        "qty",
        "item",
        "purchased",
        "purch_date",
        "notes",
    ]

    list_filter = ["shopping_list", "aisle"]

    ordering = ["shopping_list", "aisle", "item"]


class VersionAdmin(admin.ModelAdmin):
    list_display = ["version_number"]

    list_display_links = ["version_number"]

    ordering = ["version_number"]

    def has_add_permission(self, request):
        # Return False to disable adding
        return False

    def has_delete_permission(self, request, obj=None):
        # Return False to disable deleting
        return False

    def has_change_permission(self, request, obj=None):
        # Return False to disable editing
        return False


admin.site.register(Store, StoreAdmin)
admin.site.register(Aisle, AisleAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(Version, VersionAdmin)
