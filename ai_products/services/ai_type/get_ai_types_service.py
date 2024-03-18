from ai_products.models import AiType
from django.db.models.query import QuerySet


class GetAiTypesService:

    def get_ai_types(self) -> QuerySet[AiType]:
        ai_type_list = AiType.objects.all()
        return ai_type_list
