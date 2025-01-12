from django.db import models
from .ai_input import AiInput


class AiType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_inputs = models.ManyToManyField(
        AiInput, through="AiTypeAiInput", related_name="ai_types"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
