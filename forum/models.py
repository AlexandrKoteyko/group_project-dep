from django.db import models
from django.conf import settings

class ForumCategory(models.Model):
    CATEGORY_CHOICES = [
        ('maps', 'Карти'),
        ('updates', 'Оновлення та патчі'),
        ('matches', 'Обговорення матчів'),
        ('settings', 'Сетинги й конфіги'),
        ('memes', 'Меми'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.get_name_display()

class Topic(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_topics')
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']