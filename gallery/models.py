from django.db import models
from django.conf import settings

class MediaItem(models.Model):
    MEDIA_TYPES = [
        ('screenshot', 'Скріншот'),
        ('meme', 'Мем'),
        ('clip', 'Кліп'),
        ('other', 'Інше'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gallery_items')
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='gallery/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title or 'Без назви'}"