from django.db import models
from .work import Work
from .user import User
from .ai_model import AiModel
from .ai_request import AiRequest
import datetime


class Prompt(models.Model):
    ai_request = models.ForeignKey(
        AiRequest, on_delete=models.CASCADE, related_name="prompts"
    )
    prompt = models.TextField(blank=True)
    output_example_model_description = models.CharField(max_length=255, blank=True)
    output_example_model = models.JSONField(blank=True, null=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="prompts")
    ai_model = models.ForeignKey(
        AiModel, on_delete=models.CASCADE, related_name="prompts"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompts")
    order = models.IntegerField(default=1)
    token = models.IntegerField(default=0)
    cost = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)
    request_date = models.DateTimeField(default=datetime.datetime(1000, 1, 1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
