from ai_products.models import Work
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class GetWorkService:

    def get_work(self, id: int) -> Work:
        try:
            work = Work.objects.select_related("task").get(id=id)
        except Work.DoesNotExist as e:
            raise CustomApiErrorException(
                error_type=ErrorType.WORK_NOT_FOUND,
                message=f"id:{id}のWorkは存在しません。",
            )
        return work
