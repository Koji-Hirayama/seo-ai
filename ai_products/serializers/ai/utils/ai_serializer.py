from typing import Any, List
from rest_framework import serializers
from ai_products.services.ai.interface.ai_service_interface import (
    OutputExampleModel,
)
from utils.errors import RequestErrorSerializer
from ai_products.models import PromptOutput, Prompt, Work, PromptInput
from .dynamic_pydantic_model_serializer import AiOutputPydanticModelSerialiser
from pydantic import BaseModel, ValidationError
from dataclasses import dataclass


@dataclass
class AiRequestPrams:
    task_id: int
    ai_model_id: int
    ai_type_id: int
    output_example_model_description: str
    output_example_model: OutputExampleModel
    output_model_class: BaseModel
    prompt_user_input: str
    urls: List[str]


class BaseRequestPromptSerializer(RequestErrorSerializer):
    """AIの指示を受けるベースシリアライザークラス。
    追加のフィールドが必要な場合は、このクラスを継承した、シリアライザークラスを作る
    """

    task_id = serializers.IntegerField(min_value=1)
    ai_model_id = serializers.IntegerField(min_value=1)
    ai_type_id = serializers.IntegerField(min_value=1)
    output_example_model_description = serializers.CharField(
        allow_blank=True, allow_null=True
    )
    output_example_model = serializers.JSONField(allow_null=True)
    prompt_user_input = serializers.CharField(allow_blank=True, allow_null=True)
    urls = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        allow_empty=True,
    )

    def get_ai_request_params(self) -> AiRequestPrams:
        """is_valid()済み必須"""
        return AiRequestPrams(
            task_id=self.validated_data["task_id"],
            ai_model_id=self.validated_data["ai_model_id"],
            ai_type_id=self.validated_data["ai_type_id"],
            output_example_model_description=self.validated_data[
                "output_example_model_description"
            ],
            output_example_model=self.get_output_example_model(),
            output_model_class=self.get_output_model_class(),
            prompt_user_input=self.validated_data["prompt_user_input"],
            urls=self.validated_data["urls"],
        )

    def is_valid(self, *, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)
        if is_valid:
            try:
                self._output_example_model = OutputExampleModel(
                    **self.validated_data["output_example_model"]
                )
                aiOutputPydanticModelserialiser = AiOutputPydanticModelSerialiser()
                self._output_model_class = aiOutputPydanticModelserialiser.create_model(
                    self._output_example_model.model_dump()
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


class _PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = (
            "id",
            "prompt",
            "output_example_model_description",
            "output_example_model",
            "request_date",
            "token",
            "cost",
            "total_cost",
            "order",
        )


class _PromptOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptOutput
        fields = (
            "id",
            "output",
            "output_model",
            "ai_model",
            "user",
            "is_error",
            "token",
            "cost",
            "total_cost",
            "response_date",
            "order",
            "prompt",
        )


class _WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ("id", "version")


class _PromptInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptInput
        fields = (
            "id",
            "input",
            "input_text",
            "input_number",
            "output_example_model_description",
            "output_example_model",
            "result_json",
            "ai_input_id",
            "ai_input_field_id",
            "prompt_id",
        )


class AiResponseSerializer(serializers.Serializer):
    prompt = _PromptSerializer()
    prompt_output = _PromptOutputSerializer()
    prompt_inputs = _PromptInputSerializer(many=True)
    work = _WorkSerializer()
