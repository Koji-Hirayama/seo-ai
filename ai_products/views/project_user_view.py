from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.application.service.project_user import ProjectUserListService
from ai_products.infrastructure.repository.project_user import ProjectUserRepository
from ai_products.serializers.project_user import GetProjectsForUserSerializer

class GetProjectsForUserAPIView(APIView):
    def get(self, request):
        service = ProjectUserListService(ProjectUserRepository())
        project_user_list = service.get_projects_for_user(request.user.id)
        
        serializer = GetProjectsForUserSerializer(data=project_user_list.model_dump())
        if serializer.is_valid():
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)