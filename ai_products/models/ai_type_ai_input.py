from django.db import models
from ai_products.models import AiInput, AiType


class AiTypeAiInput(models.Model):
    ai_input = models.ForeignKey(
        AiInput, on_delete=models.CASCADE, related_name="ai_type_ai_inputs"
    )
    ai_type = models.ForeignKey(
        AiType, on_delete=models.CASCADE, related_name="ai_type_ai_inputs"
    )
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ai_type.name}--{self.ai_input.name}--{self.order}"
