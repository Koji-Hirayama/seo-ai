from .task import Task
from django.db import models


class Work(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="works")
    version = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    