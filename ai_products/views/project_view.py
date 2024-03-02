from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.service.project import CreateProjectService
from drf_spectacular.utils import extend_schema
from ai_products.serializers.project.project_serializer import CreateProjectSerializer, RequestCreateProjectSerializer



class CreateProjectAPIView(APIView):
    
    @extend_schema(request=RequestCreateProjectSerializer, responses={201: CreateProjectSerializer})
    def post(self, request):
        serializer = RequestCreateProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        project_name = serializer.validated_data.get("name")
        service = CreateProjectService()
        project = service.create_project(user=request.user, project_name=project_name)
        serializer = CreateProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        