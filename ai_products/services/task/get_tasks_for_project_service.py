from ai_products.models import Project
from utils.errors import ErrorType, CustomApiErrorException


class GetTasksForProjectService:
    def get_tasks_for_project(self, project_id: int) -> Project:
        try:
            project_tasks = Project.objects.prefetch_related("tasks").get(id=project_id)
            return project_tasks
        except Project.DoesNotExist:
            raise CustomApiErrorException(
                error_type=ErrorType.PROJECT_NOT_FOUND,
                message=f"id:{project_id}のProjectは存在しません。",
            )
