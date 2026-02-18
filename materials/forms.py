from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('title', 'description', 'category', 'file', 'link', 'youtube_embed')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва матеріалу'
            }),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'class': 'form-control',
                'placeholder': 'Опис матеріалу...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'youtube_embed': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Вставте HTML код для вбудовування YouTube (<iframe>...</iframe>)'
            }),
        }
        labels = {
            'title': 'Назва',
            'description': 'Опис',
            'category': 'Категорія',
            'file': 'Файл',
            'link': 'Посилання',
            'youtube_embed': 'YouTube вбудовування',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        link = cleaned_data.get('link')
        youtube_embed = cleaned_data.get('youtube_embed')
        
        # Перевіряємо, що є хоча б один спосіб завантаження/перегляду
        if not any([file, link, youtube_embed]):
            raise forms.ValidationError('Потрібно завантажити файл, вказати посилання або додати YouTube вбудовування.')
        
        return cleaned_data