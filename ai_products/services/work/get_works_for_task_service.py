from ai_products.models import Work
from django.db.models.query import QuerySet


class GetWorksForTaskService:
    def get_works_for_task(self, task_id: int) -> QuerySet[Work]:
        works = Work.objects.filter(task_id=task_id)
        return works
