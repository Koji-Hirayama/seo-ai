from django.db import models
from ai_products.models.user import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through="ProjectUser", related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name
