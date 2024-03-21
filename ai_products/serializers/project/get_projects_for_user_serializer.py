from rest_framework import serializers
from ai_products.models import Project
from ai_products.models import ProjectUser
from ai_products.serializers import UserSerializer


class _ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "users")


class GetProjectsForUserSerializer(serializers.ModelSerializer):
    project = _ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectUser
        fields = ("id", "project", "is_admin")
