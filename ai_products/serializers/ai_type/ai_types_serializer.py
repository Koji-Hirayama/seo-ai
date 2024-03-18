from rest_framework import serializers
from ai_products.models import AiType


class AiTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiType
        fields = ("id", "name", "description")
