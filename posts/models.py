from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    MEDIA_CHOICES = [
        ('image', 'Зображення'),
        ('video', 'Відео'),
        ('demo', 'Демо-файл'),
        ('none', 'Без медіа'),
    ]
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(validators=[MaxLengthValidator(280)], verbose_name="Текст поста")
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='none')
    media_file = models.FileField(upload_to='posts/media/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(validators=[MaxLengthValidator(500)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username}"