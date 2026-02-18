from django.contrib import admin
from .models import Vote, VoteOption, UserVote

class VoteOptionInline(admin.TabularInline):
    model = VoteOption
    extra = 1

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'vote_type', 'is_active', 'created_at')
    list_filter = ('vote_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [VoteOptionInline]

@admin.register(VoteOption)
class VoteOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'vote', 'votes')
    list_filter = ('vote',)
    search_fields = ('text',)

@admin.register(UserVote)
class UserVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'vote', 'option', 'voted_at')
    list_filter = ('voted_at',)
    search_fields = ('user__username', 'vote__title')