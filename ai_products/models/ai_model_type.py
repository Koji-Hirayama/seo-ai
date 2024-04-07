from django.db import models


class AiModelType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
