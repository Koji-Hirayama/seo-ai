from typing import Any
from rest_framework import serializers
from ai_products.models import Project
from ai_products.models import ProjectUser
from ai_products.serializers import UserSerializer
from utils.errors import RequestErrorSerializer


# Postで受け取る値用
class RequestCreateProjectSerializer(RequestErrorSerializer):
    name = serializers.CharField(max_length=255)

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()


class _ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "users")


class CreateProjectSerializer(serializers.ModelSerializer):
    project = _ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectUser
        fields = ("id", "project", "is_admin")
