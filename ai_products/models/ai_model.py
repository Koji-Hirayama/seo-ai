from django.db import models
from .api_provider import ApiProvider
from .ai_model_type import AiModelType


class AiModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    ai_model_type = models.ForeignKey(
        AiModelType, on_delete=models.CASCADE, related_name="ai_models"
    )
    api_provider = models.ForeignKey(
        ApiProvider, on_delete=models.CASCADE, related_name="ai_models"
    )
    token_limit = models.IntegerField(default=0)
    input_token_cost = models.FloatField(default=0)
    output_token_cost = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
