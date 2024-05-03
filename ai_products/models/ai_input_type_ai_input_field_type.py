from django.db import models
from ai_products.models import AiInputType, AiInputFieldType


class AiInputTypeAiInputFieldType(models.Model):
    ai_input_type = models.ForeignKey(
        AiInputType,
        on_delete=models.CASCADE,
        related_name="ai_input_type_ai_input_field_types",
    )
    ai_input_field_type = models.ForeignKey(
        AiInputFieldType,
        on_delete=models.CASCADE,
        related_name="ai_input_type_ai_input_field_types",
    )
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"{self.ai_input_type.name}--{self.ai_input_field_type.name}--{self.order}"
        )
