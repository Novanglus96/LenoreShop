from django.contrib import admin
from .models import (
    Store,
    Aisle,
    Item,
    ShoppingList,
    ListItem,
    Freezer,
    FreezerItem,
    FreezerLog,
    Version,
)

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


class FreezerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "location"]

    search_fields = ["name", "location"]

    ordering = ["name"]


class FreezerItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "freezer",
        "name",
        "qty",
        "unit",
        "date_added",
        "discard_date",
        "notes",
    ]

    list_filter = ["freezer", "discard_date"]

    search_fields = ["name"]

    ordering = ["freezer", "discard_date", "name"]


class FreezerLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "occurred",
        "action",
        "name",
        "qty",
        "unit",
        "freezer_name",
        "to_freezer_name",
    ]

    list_filter = ["action", "freezer_name"]

    search_fields = ["name"]

    # The history is a record of what happened, so the admin reads it rather
    # than rewrites it. Entries are written by the API handlers only.
    readonly_fields = [
        "action",
        "name",
        "qty",
        "unit",
        "freezer_name",
        "to_freezer_name",
        "freezer",
        "freezeritem",
        "occurred",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


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
admin.site.register(Freezer, FreezerAdmin)
admin.site.register(FreezerItem, FreezerItemAdmin)
admin.site.register(FreezerLog, FreezerLogAdmin)
admin.site.register(Version, VersionAdmin)
