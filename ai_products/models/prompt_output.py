from django.db import models
from .llm import Llm
from .prompt import Prompt

class PromptOutput(models.Model):
    text = models.TextField(blank=True)
    json = models.JSONField(blank=True, null=True)
    order = models.IntegerField()
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="prompt_outputs")
    llm = models.ForeignKey(Llm, on_delete=models.CASCADE, related_name="prompt_outputs")
    text_length = models.IntegerField()
    json_length = models.IntegerField()
    token = models.IntegerField()
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    