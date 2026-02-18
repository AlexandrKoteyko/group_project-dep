from django.db import models
from django.conf import settings

class Vote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    vote_type = models.CharField(max_length=50, choices=[
        ('highlight', 'Найкращий хайлайт дня'),
        ('post', 'Топ пост тижня'),
        ('weapon', 'Краще a1 чи a4?'),
        ('other', 'Інше'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class VoteOption(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='votes/', blank=True, null=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class UserVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    option = models.ForeignKey(VoteOption, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'vote']