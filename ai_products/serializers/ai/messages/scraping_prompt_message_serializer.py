from rest_framework import serializers
from utils.errors import RequestErrorSerializer


class RequestScrapingPromptMessageSeriaizer(RequestErrorSerializer):
    urls = serializers.ListField(child=serializers.CharField())
    input = serializers.CharField(max_length=255)


class ScrapingPromptMessageSeriaizer(serializers.Serializer):
    prompt = serializers.CharField()
