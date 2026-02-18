from django import forms
from django.core.mail import send_mail
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть ваше ім'я"
        })
    )
    email = forms.EmailField(
        label="Ваш email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )
    subject = forms.CharField(
        max_length=200,
        label="Тема",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Тема повідомлення'
        })
    )
    message = forms.CharField(
        label="Повідомлення",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Ваше повідомлення...'
        })
    )
    
    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        full_message = f"Повідомлення від: {name} ({email})\n\n{message}"
        
        send_mail(
            subject=f'CS2 MicroTwitter: {subject}',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )