from django.contrib import admin
from .models import Post, Comment, Hashtag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_content', 'author', 'media_type', 'is_pinned', 'created_at')
    list_filter = ('media_type', 'is_pinned', 'created_at')
    search_fields = ('content', 'author__username')
    filter_horizontal = ('hashtags',)
    readonly_fields = ('created_at', 'updated_at')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Зміст'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_content', 'author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__content')
    readonly_fields = ('created_at', 'updated_at')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Коментар'

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)