from typing import Any
from rest_framework import serializers
from ai_products.domains.ai.ai_request_data.ai_request_datas import AiRequestDatas
from ai_products.domains.ai.ai_request_params import AiRequestParams
from utils.errors import RequestErrorSerializer
from ai_products.models import PromptOutput, Prompt, Work, PromptInput, AiRequest, Task


class BaseRequestPromptSerializer(RequestErrorSerializer):
    """AIの指示を受けるベースシリアライザークラス。
    追加のフィールドが必要な場合は、このクラスを継承した、シリアライザークラスを作る
    """

    task_id = serializers.IntegerField(min_value=1)
    work_id = serializers.IntegerField(min_value=1)
    ai_type_id = serializers.IntegerField(min_value=1)
    request_data = serializers.JSONField()

    def get_ai_request_params(self) -> AiRequestParams:
        """is_valid()済み必須"""

        return AiRequestParams(
            task_id=self.validated_data["task_id"],
            work_id=self.validated_data["work_id"],
            ai_type_id=self.validated_data["ai_type_id"],
            request_data=AiRequestDatas(**self.validated_data["request_data"]),
        )

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()


class _TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "description")


class _WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ("id", "version")


class _AiRequestSerializer(serializers.ModelSerializer):
    task = _TaskSerializer(read_only=True)
    work = _WorkSerializer(read_only=True)

    class Meta:
        model = AiRequest
        fields = (
            "id",
            "task",
            "work",
            "user",
            "request_data",
            "status",
        )


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
    ai_request = _AiRequestSerializer()
    prompt = _PromptSerializer()
    prompt_output = _PromptOutputSerializer()
    prompt_inputs = _PromptInputSerializer(many=True)
