from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'downloads', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('downloads', 'created_at', 'updated_at')