from django.db import models
from .schedule_type import ScheduleType
from .task import Task

class Schedule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="schedules")
    schedule_type = models.ForeignKey(ScheduleType, on_delete=models.CASCADE, related_name="schedules")
    status = models.IntegerField() #0:実行、1:停止
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    