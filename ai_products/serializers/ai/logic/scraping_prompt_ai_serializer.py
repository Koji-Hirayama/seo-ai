from ai_products.serializers.ai.utils.ai_serializer import (
    BaseRequestPromptSerializer,
)
from rest_framework import serializers


class RequestScrapingPromptAiSerializer(BaseRequestPromptSerializer):
    url = serializers.CharField()
