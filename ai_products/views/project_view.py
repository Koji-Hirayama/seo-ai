from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.application.service.project import CreateProjectService
from ai_products.infrastructure.repository.project import ProjectRepository
from ai_products.infrastructure.repository.project_user import ProjectUserRepository
from ai_products.serializers.project import RequestCreateProjectSerializer, CreateProjectSerializer
from ai_products.domain.project import Project as DomainProject



class CreateProjectAPIView(APIView):
    def post(self, request):
        request_serializer = RequestCreateProjectSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = CreateProjectService(
            project_repository=ProjectRepository(),
            project_user_repository=ProjectUserRepository()
        )
        project_name = request_serializer.validated_data.get("name")
        project = DomainProject(name=project_name)
        login_user = request.user.to_domain()
        project = service.create_project(project=project, user=login_user)
        serializer = CreateProjectSerializer(data=project.model_dump())
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            