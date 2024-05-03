from rest_framework import serializers
from ai_products.models import AiInput, AiInputField, AiTypeAiInput, AiInputType
from utils.errors import RequestErrorSerializer


class RequestAiTypeInputFieldsSerializer(RequestErrorSerializer):
    ai_type_id = serializers.IntegerField(min_value=1)


class _AiInputField(serializers.ModelSerializer):
    class Meta:
        model = AiInputField
        fields = ("id", "name", "description", "question", "context", "order")


class _AiInputType(serializers.ModelSerializer):
    class Meta:
        model = AiInputType
        fields = ("id", "name")


class _AiInput(serializers.ModelSerializer):
    ai_input_type = _AiInputType(read_only=True)
    ai_input_fields = _AiInputField(read_only=True, many=True)

    class Meta:
        model = AiInput
        fields = ("id", "name", "description", "ai_input_type", "ai_input_fields")


class GetAiTypeInputFieldsSerializer(serializers.ModelSerializer):
    ai_input = _AiInput(read_only=True)

    class Meta:
        model = AiTypeAiInput
        fields = ("id", "ai_type", "ai_input", "order")
