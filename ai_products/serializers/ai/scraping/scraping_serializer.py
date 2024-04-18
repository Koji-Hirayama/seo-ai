from rest_framework import serializers
from utils.errors import RequestErrorSerializer


class RequestScrapingSerializer(RequestErrorSerializer):
    urls = serializers.ListField(child=serializers.CharField())


class ScrapingSerialize(serializers.Serializer):
    url = serializers.CharField()
    result = serializers.CharField()
