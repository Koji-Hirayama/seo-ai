from rest_framework import serializers
from ..custom_serializers import ResponseSerializer

class _UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField(max_length=50)
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()
    
class _ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    users = _UserSerializer(many=True)
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()
    # deleted_at = serializers.DateTimeField(allow_null=True)
    
class _ProjectUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # user = _UserSerializer()
    project = _ProjectSerializer()
    is_admin = serializers.BooleanField()
    

class GetProjectsForUserSerializer(ResponseSerializer):
    project_user_list = _ProjectUserSerializer(many=True)
    

