from django.db import models


class PromptType(models.Model):
    name = models.CharField(max_length=255)
    