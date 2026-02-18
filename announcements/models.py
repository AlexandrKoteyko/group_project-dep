from django.db import models
from django.conf import settings

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    announcement_type = models.CharField(max_length=50, choices=[
        ('tournament', 'Турніри'),
        ('server', 'Новини сервера'),
        ('rules', 'Правила'),
        ('update', 'Оновлення'),
    ])
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title