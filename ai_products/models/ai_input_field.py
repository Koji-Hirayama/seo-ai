from django.db import models
from .ai_input_field_type import AiInputFieldType
from .ai_input import AiInput


class AiInputField(models.Model):
    name = models.CharField(max_length=255)
    ai_input_field_type = models.ForeignKey(
        AiInputFieldType,
        on_delete=models.CASCADE,
        related_name="ai_input_fields",
    )
    ai_input = models.ForeignKey(
        AiInput,
        on_delete=models.CASCADE,
        related_name="ai_input_fields",
    )
    description = models.TextField(blank=True)
    question = models.CharField(max_length=255, blank=True)
    context = models.TextField(blank=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}--{self.ai_input.name}--{self.order}"
