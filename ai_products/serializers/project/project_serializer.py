from rest_framework import serializers
from ai_products.models.project import Project

# Postで受け取る値用
class RequestCreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    
class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name")