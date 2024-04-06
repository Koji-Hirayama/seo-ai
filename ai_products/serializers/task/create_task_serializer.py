from typing import Any
from rest_framework import serializers
from utils.errors import RequestErrorSerializer
from ai_products.models import Task


class RequestCreateTaskSerializer(RequestErrorSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    project_id = serializers.IntegerField(min_value=1)
    ai_type_id = serializers.IntegerField(min_value=1)
    is_save = serializers.BooleanField(default=False)

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "description", "ai_type", "is_save")
