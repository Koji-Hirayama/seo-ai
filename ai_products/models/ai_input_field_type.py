from django.db import models


class AiInputFieldType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    context_parameters_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
