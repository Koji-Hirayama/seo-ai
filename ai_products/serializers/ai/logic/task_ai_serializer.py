from ai_products.serializers.ai.utils.ai_serializer import (
    BaseRequestPromptSerializer,
)
from rest_framework import serializers


class RequestTaskAiSerializer(BaseRequestPromptSerializer):
    urls = serializers.ListField(child=serializers.CharField())
