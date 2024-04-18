from rest_framework import serializers
from ai_products.models import AiModel, AiModelType, ApiProvider


class _AiModelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiModelType
        fields = ("id", "name", "description", "label")


class _ApiProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiProvider
        fields = ("id", "name")


class AiModelSerialiser(serializers.ModelSerializer):
    ai_model_type = _AiModelTypeSerializer(read_only=True)
    api_provider = _ApiProviderSerializer(read_only=True)

    class Meta:
        model = AiModel
        fields = ("id", "name", "description", "label", "ai_model_type", "api_provider")
