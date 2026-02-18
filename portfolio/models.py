from django.db import models
from django.conf import settings

class PortfolioItem(models.Model):
    ITEM_TYPES = [
        ('screenshot', 'Скріншот'),
        ('demo', 'Демо'),
        ('video', 'Відео'),
        ('highlight', 'Хайлайт'),
    ]
    
    ROLES = [
        ('rifler', 'Rifler'),
        ('awper', 'AWPer'),
        ('lurker', 'Lurker'),
        ('support', 'Support'),
        ('igl', 'IGL (In-Game Leader)'),
        ('entry', 'Entry Fragger'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    file = models.FileField(upload_to='portfolio/')
    role = models.CharField(max_length=20, choices=ROLES, blank=True)
    game_map = models.CharField(max_length=50, blank=True, help_text="Карта на якій зроблено хайлайт")
    weapon = models.CharField(max_length=50, blank=True, help_text="Зброя, яка була використана")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"