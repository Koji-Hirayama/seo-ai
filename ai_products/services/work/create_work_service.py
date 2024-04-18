from ai_products.models import Work, Task
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class CreateWorkService:
    def create_work(self, task_id: int) -> Work:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_WORK_ELEMENT_NOT_FOUND,
                message="Workの作成に失敗しました。",
                error_details=[
                    ErrorDetail(
                        field="task", message=f"id:{task_id}のTaskは存在しません。"
                    )
                ],
            )

        work = Work(task=task, version=0)
        work.save()
        return work
