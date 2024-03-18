from typing import Any
from rest_framework import serializers
from ai_products.models.project import Project
from utils.errors import RequestErrorSerializer


# Postで受け取る値用
class RequestCreateProjectSerializer(RequestErrorSerializer):
    name = serializers.CharField(max_length=255)

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name")
