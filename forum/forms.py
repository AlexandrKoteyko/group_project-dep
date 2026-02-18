from django import forms
from .models import Topic, Message

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('category', 'title', 'content')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок теми'
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Опишіть тему детально...'
            })
        }
        labels = {
            'category': 'Категорія',
            'title': 'Заголовок',
            'content': 'Зміст',
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Ваша відповідь...'
            })
        }
        labels = {
            'text': 'Повідомлення'
        }