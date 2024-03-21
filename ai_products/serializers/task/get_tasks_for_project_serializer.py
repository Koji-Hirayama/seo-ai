from rest_framework import serializers
from ai_products.models import Project, Task


class _TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "description", "ai_type")


class GetTaskForProjectSerializer(serializers.ModelSerializer):
    tasks = _TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "tasks")
