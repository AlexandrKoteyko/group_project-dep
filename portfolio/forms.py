from django import forms
from .models import PortfolioItem

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ('title', 'description', 'item_type', 'file', 'role', 'game_map', 'weapon')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва хайлайту'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Опишіть свій хайлайт...'
            }),
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'game_map': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: Mirage, Dust2, Inferno'
            }),
            'weapon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: AWP, AK-47, M4A1-S'
            }),
        }
        labels = {
            'title': 'Назва',
            'description': 'Опис',
            'item_type': 'Тип вмісту',
            'file': 'Файл',
            'role': 'Роль у грі',
            'game_map': 'Карта',
            'weapon': 'Зброя',
        }