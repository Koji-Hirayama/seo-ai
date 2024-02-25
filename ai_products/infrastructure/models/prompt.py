from django.db import models
from .llm import Llm
from .prompt_type import PromptType
from .work import Work


class Prompt(models.Model):
    text = models.TextField()
    prompt_type = models.ForeignKey(PromptType, on_delete=models.CASCADE, related_name="prompts")
    order = models.IntegerField()
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="prompts")
    llm = models.ForeignKey(Llm, on_delete=models.CASCADE, related_name="prompts")
    text_length = models.IntegerField()
    token = models.IntegerField()
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    