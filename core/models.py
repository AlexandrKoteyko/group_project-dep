from django.db import models

class SiteInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
