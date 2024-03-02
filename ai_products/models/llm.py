from django.db import models
from .api_provider import ApiProvider
from .llm_type import LlmType

class Llm(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    llm_type = models.ForeignKey(LlmType, on_delete=models.CASCADE, related_name="llms")
    api_provider = models.ForeignKey(ApiProvider, on_delete=models.CASCADE, related_name="llms")
    created_at = models.DateTimeField(auto_now_add=True)
    