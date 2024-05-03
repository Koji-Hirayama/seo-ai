from ai_products.models import AiInputField
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class GetAiInputFieldService:
    def get_ai_input_field(self, id: int) -> AiInputField:
        try:
            ai_input_field = AiInputField.objects.get(id=id)
        except AiInputField.DoesNotExist as e:
            raise CustomApiErrorException(
                error_type=ErrorType.AI_INPUT_FIELD_NOT_FOUND,
                message=f"id:{id}のAiModelは存在しません。",
            )
        return ai_input_field
