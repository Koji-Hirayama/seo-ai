from rest_framework import serializers
from ai_products.models import Task, AiType


class _AiTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiType
        fields = ("id", "name", "description")


class GetTasksForProjectSerializer(serializers.ModelSerializer):
    ai_type = _AiTypeSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "name", "description", "ai_type", "is_save")
