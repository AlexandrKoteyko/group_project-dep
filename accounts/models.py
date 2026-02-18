from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Користувач'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    steam_profile = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_moderator(self):
        return self.role in ['moderator','admin']
    
    def is_admin(self):
        return self.role == 'admin'
