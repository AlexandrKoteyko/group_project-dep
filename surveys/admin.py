from django.contrib import admin
from .models import Survey, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'is_multi_page', 'created_at')
    list_filter = ('is_active', 'is_multi_page', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'page', 'order')
    list_filter = ('survey', 'page')
    search_fields = ('text',)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'votes')
    list_filter = ('question__survey',)
    search_fields = ('text',)