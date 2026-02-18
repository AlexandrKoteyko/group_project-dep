from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'location', 'is_active')
    list_filter = ('event_type', 'is_active', 'date')
    search_fields = ('title', 'description', 'location')