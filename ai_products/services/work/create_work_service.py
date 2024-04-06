from ai_products.models import Work, Task
from utils.errors import CustomApiErrorException, ErrorType


class CreateWorkService:
    def create_work(self, task_id: int) -> Work:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise CustomApiErrorException(
                error_type=ErrorType.TASK_NOT_FOUND,
                message=f"id:{task_id}のTaskは存在しません。",
            )

        work = Work(task=task)
        work.save()
        return work
