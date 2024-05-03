from django.db import models
from .schedule import Schedule
from .work import Work
from .task import Task


class ScheduleLog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="schedule_logs"
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="schedule_logs"
    )
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, related_name="schedule_logs"
    )
    start_date = models.DateTimeField(verbose_name="開始日")
    end_date = models.DateTimeField(verbose_name="終了日")
    status = models.IntegerField()  # 0:予約、1:実行開始、2:実行完了、3:停止
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
