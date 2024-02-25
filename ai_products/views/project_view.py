from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.application.service.project import CreateProjectService
from ai_products.infrastructure.repository.project import ProjectRepository
from ai_products.serializers.project import RequestCreateProjectSerializer, CreateProjectSerializer



class CreateProjectAPIView(APIView):
    def post(self, request):
        request_serializer = RequestCreateProjectSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        name = request_serializer.validated_data.get("name")
        user_id = request.user.id
        
        service = CreateProjectService(ProjectRepository())
        project = service.create_project(name=name, user_id=user_id)
        
        serializer = CreateProjectSerializer(data=project.model_dump())
        if serializer.is_valid():
            data = serializer.validated_data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        