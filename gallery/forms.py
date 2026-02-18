from django import forms
from .models import MediaItem

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ('title', 'file', 'media_type', 'description')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва медіа (необов\'язково)'
            }),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Опис медіа'
            }),
        }
        labels = {
            'title': 'Назва',
            'file': 'Файл',
            'media_type': 'Тип медіа',
            'description': 'Опис',
        }