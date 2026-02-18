from django.db import models

class Event(models.Model):
    EVENT_TYPES = [
        ('patch', 'Випуск патчу'),
        ('tournament', 'Турнір'),
        ('competition', 'Конкурс'),
        ('other', 'Інше'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title