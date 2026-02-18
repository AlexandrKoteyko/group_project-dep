from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content', 'announcement_type', 'is_pinned')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок оголошення'
            }),
            'content': forms.Textarea(attrs={
                'rows': 8,
                'class': 'form-control',
                'placeholder': 'Текст оголошення...'
            }),
            'announcement_type': forms.Select(attrs={'class': 'form-control'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Зміст',
            'announcement_type': 'Тип оголошення',
            'is_pinned': 'Закріпити',
        }