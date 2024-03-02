from django.db import models
from .prompt_output import PromptOutput
from .work import Work
from .task import Task


class OutputResult(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="output_results")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="output_results")
    prompt_output = models.ForeignKey(PromptOutput, on_delete=models.CASCADE, related_name="output_results")
    json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    