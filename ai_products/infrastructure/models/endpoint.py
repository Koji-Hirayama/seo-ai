from django.db import models
from .task import Task
from .output_result import OutputResult

class Endpoint(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="endpoints")
    output_result = models.ForeignKey(OutputResult, on_delete=models.CASCADE, related_name="endpoints")
    endpoint = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)