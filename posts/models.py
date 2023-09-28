from django.db import models
from django.utils import timezone


class Articles(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="images", blank=True, null=True)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title