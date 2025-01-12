from django.db import models
from ai_products.models.user import User
from .ai_type import AiType
from .project import Project


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_type = models.ForeignKey(AiType, on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    is_save = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
