from typing import Any
from rest_framework import serializers
from ai_products.services.ai.interface.ai_logic_service_interface import (
    OutputExampleModel,
)
from utils.errors import RequestErrorSerializer
from ai_products.models import PromptOutput
from .dynamic_pydantic_model_serializer import AiOutputPydanticModelSerialiser
from pydantic import BaseModel, ValidationError


class BaseRequestPromptSerializer(RequestErrorSerializer):
    """AIの指示を受けるベースシリアライザークラス。
    追加のフィールドが必要な場合は、このクラスを継承した、シリアライザークラスを作る
    """

    input = serializers.CharField()
    output_example_model_description = serializers.CharField()
    output_example_model = serializers.JSONField()
    work_id = serializers.IntegerField(min_value=1)
    llm_id = serializers.IntegerField(min_value=1)

    def is_valid(self, *, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)
        if is_valid:
            try:
                self._output_example_model = OutputExampleModel(
                    **self.validated_data["output_example_model"]
                )
                aiOutputPydanticModelserialiser = AiOutputPydanticModelSerialiser()
                self._output_model_class = aiOutputPydanticModelserialiser.create_model(
                    self.validated_data["output_example_model"]
                )
            except ValidationError:
                self.create_error_detail(
                    "output_example_model", "正しくて定義されていません。"
                )
                is_valid = False

        return is_valid

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()

    # pydandictで返す
    def get_output_example_model(self) -> OutputExampleModel:
        """is_valid()済み必須"""
        return self._output_example_model

    # output_example_modelを元に、AIアウトプットのModelクラス作成して返す
    def get_output_model_class(self) -> BaseModel:
        """is_valid()済み必須"""
        return self._output_model_class


class AiResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptOutput
        fields = (
            "id",
            "output",
            "output_model",
            "prompt",
            "llm",
            "user",
            "is_error",
            "token",
            "cost",
            "total_cost",
            "response_date",
        )
