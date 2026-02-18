from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Біографія'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'avatar', 'steam_profile')
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Email',
            'avatar': 'Аватар',
            'steam_profile': 'Steam профіль',
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'avatar', 'steam_profile', 'role')
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Email',
            'bio': 'Біографія',
            'avatar': 'Аватар',
            'steam_profile': 'Steam профіль',
            'role': 'Роль',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'avatar', 'steam_profile')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'steam_profile': forms.URLInput(attrs={'class': 'form-control'}),
        }