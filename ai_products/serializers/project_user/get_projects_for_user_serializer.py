from rest_framework import serializers
from ai_products.models import Project
from ai_products.models import ProjectUser
from ai_products.serializers.user.user_serializer import UserSerializer



        
class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'users')
        
    
class ProjectUserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = ProjectUser
        fields = "__all__"
    

