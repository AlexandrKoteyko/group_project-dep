from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'event_type', 'description', 'date', 'end_date', 'location', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Назва події',
            'event_type': 'Тип події',
            'description': 'Опис',
            'date': 'Дата початку',
            'end_date': 'Дата закінчення',
            'location': 'Місце',
            'image': 'Зображення',
        }