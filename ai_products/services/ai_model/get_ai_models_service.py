from ai_products.models import AiModel
from django.db.models.query import QuerySet
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class GetAiModelService:

    def get_ai_model(self, id: int) -> AiModel:
        try:
            ai_model = AiModel.objects.select_related(
                "ai_model_type", "api_provider"
            ).get(id=id)
        except AiModel.DoesNotExist as e:
            raise CustomApiErrorException(
                error_type=ErrorType.AI_MODEL_NOT_FOUND,
                message=f"id:{ai_model}のAiModelは存在しません。",
            )
        return ai_model

    def get_ai_models(self) -> QuerySet[AiModel]:
        ai_model_list = AiModel.objects.select_related(
            "ai_model_type", "api_provider"
        ).all()
        return ai_model_list
