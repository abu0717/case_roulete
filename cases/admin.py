from django.contrib import admin
from .models import Case, CaseItem, UserInventory


class ItemInline(admin.TabularInline):
    model = CaseItem
    extra = 1


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    inlines = [ItemInline]


@admin.register(CaseItem)
class CaseItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'case', 'rarity', 'chance')
    list_filter = ('case', 'rarity')
    search_fields = ('name',)
    ordering = ('case', 'rarity')
    list_per_page = 20


@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'received_at')
    list_filter = ('user', 'item')
    search_fields = ('user__username', 'item__name')
    ordering = ('user', 'received_at')
    list_per_page = 20





























