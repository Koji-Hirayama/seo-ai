from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.application.service.project import CreateProjectService
from ai_products.infrastructure.repository.project import ProjectRepository
from ai_products.infrastructure.repository.project_user import ProjectUserRepository
from ai_products.serializers.project import RequestCreateProjectSerializer, CreateProjectSerializer
from ai_products.domain.project import Project as DomainProject
from drf_spectacular.utils import extend_schema



class CreateProjectAPIView(APIView):
    
    @extend_schema(request=RequestCreateProjectSerializer, responses={201: CreateProjectSerializer})
    def post(self, request):
        serializer = RequestCreateProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = CreateProjectService(
            project_repository=ProjectRepository(),
            project_user_repository=ProjectUserRepository()
        )
        project_name = serializer.validated_data.get("name")
        project = DomainProject(name=project_name)
        login_user = request.user.to_domain()
        project = service.create_project(project=project, user=login_user)
        serializer = CreateProjectSerializer(data=project.model_dump())
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        