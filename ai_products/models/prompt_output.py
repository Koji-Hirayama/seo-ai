import datetime
from django.db import models
from .prompt import Prompt
from .work import Work
from .user import User
from .ai_model import AiModel


class PromptOutput(models.Model):
    output = models.TextField(blank=True)
    output_model = models.JSONField(blank=True, null=True)
    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="prompt_outputs"
    )
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, related_name="prompt_outputs"
    )
    ai_model = models.ForeignKey(
        AiModel, on_delete=models.CASCADE, related_name="prompt_outputs"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="prompt_outputs"
    )
    order = models.IntegerField(default=1)
    token = models.IntegerField(default=0)
    cost = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)
    is_error = models.BooleanField(default=False)
    response_date = models.DateTimeField(default=datetime.datetime(1000, 1, 1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
