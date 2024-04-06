from ai_products.models import Task
from django.db.models.query import QuerySet


class GetTasksForProjectService:
    def get_tasks_for_project(self, project_id: int) -> QuerySet[Task]:
        tasks = Task.objects.filter(project_id=project_id).select_related("ai_type")
        return tasks
