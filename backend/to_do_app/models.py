from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    # created_at = models.DateTimeField(default=timezone.now)
    # finished_at = models.DateTimeField(blank=True, null=True, default=None)
    # full_time = models.DateTimeField(blank=True, null=True, default=None)
    created_at = models.CharField(max_length=100, null=True, blank=True)
    finished_at = models.CharField(max_length=100, null=True, blank=True)
    full_time = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name