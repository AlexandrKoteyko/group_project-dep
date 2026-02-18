from django.contrib import admin
from .models import PortfolioItem

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'item_type', 'role', 'is_approved', 'created_at')
    list_filter = ('item_type', 'role', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at',)
    
    actions = ['approve_items']
    
    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
    approve_items.short_description = "Схвалити вибрані елементи"