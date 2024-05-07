from django.db import models
from .work import Work
from .user import User
from .ai_type import AiType
from .task import Task


class AiRequest(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="ai_requests")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="ai_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_requests")
    request_data = models.JSONField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
