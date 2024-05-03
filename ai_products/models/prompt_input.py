from django.db import models
from ai_products.models import Prompt, AiInput, AiInputField


class PromptInput(models.Model):
    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="prompt_inputs"
    )
    ai_input = models.ForeignKey(
        AiInput, on_delete=models.CASCADE, related_name="prompt_inputs"
    )
    ai_input_field = models.ForeignKey(
        AiInputField, on_delete=models.CASCADE, related_name="prompt_inputs"
    )
    input = models.CharField(max_length=255, blank=True)
    input_text = models.TextField(blank=True)
    input_number = models.IntegerField(default=0)
    output_example_model_description = models.CharField(max_length=255, blank=True)
    output_example_model = models.JSONField(blank=True, null=True)
    result_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
