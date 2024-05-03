from utils.errors import ErrorType, CustomApiErrorException, ErrorDetail

from ai_products.models import (
    AiTypeAiInput,
    AiInputField,
)
from django.db.models import Prefetch
from django.db import DatabaseError


class GetAiTypeInputFieldsService:
    def get_ai_type_input_fields(self, ai_type_id: int):
        try:
            ai_type_ai_inputs = (
                AiTypeAiInput.objects.filter(ai_type_id=ai_type_id)
                .select_related(
                    "ai_input", "ai_input__ai_input_type"
                )  # AiInput へのリンクを先読み
                .prefetch_related(
                    Prefetch(
                        "ai_input__ai_input_fields",  # AiInput にリンクされている AiInputField を先読み
                        queryset=AiInputField.objects.order_by(
                            "order"
                        ),  # order でソート
                    )
                )
                .order_by("order")
            )
            if not ai_type_ai_inputs.exists():
                raise CustomApiErrorException(
                    error_type=ErrorType.AI_TYPE_AI_INPUT_NOT_FOUND,
                    message="指定されたAiTypeのIDに対応するAiTypeAiInputが存在しません。",
                    error_details=[
                        ErrorDetail(
                            field="ai_type_id",
                            message=f"id:{ai_type_id}に該当するAiTypeAiInputは存在しません。",
                        )
                    ],
                )
        except DatabaseError:
            raise CustomApiErrorException(
                error_type=ErrorType.DATABASE_INTERNAL_SERVER_ERROR,
                message="get_ai_type_input_fieldsでデータベースエラーが発生しました",
            )

        return ai_type_ai_inputs
