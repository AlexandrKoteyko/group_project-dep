from django.contrib import admin
from .models import MediaItem

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'media_type', 'is_approved', 'likes', 'created_at')
    list_filter = ('media_type', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('likes', 'created_at')
    
    actions = ['approve_media']
    
    def approve_media(self, request, queryset):
        queryset.update(is_approved=True)
    approve_media.short_description = "Схвалити вибрані медіа"