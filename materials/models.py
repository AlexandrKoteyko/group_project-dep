from django.db import models

class Material(models.Model):
    CATEGORY_CHOICES = [
        ('configs', 'Конфіги (cfg-файли)'),
        ('guides', 'Гайди'),
        ('tutorials', 'Відеоуроки'),
        ('training', 'Тренування aim/recoil'),
        ('demos', 'Демки з турнірів'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    youtube_embed = models.TextField(blank=True, help_text="HTML код для вбудовування YouTube")
    downloads = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title