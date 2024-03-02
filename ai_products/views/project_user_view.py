from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.service.project_user import ProjectUserListService
from ai_products.serializers.project_user import ProjectUserSerializer
from drf_spectacular.utils import extend_schema

class GetProjectsForUserAPIView(APIView):
    
    @extend_schema(responses={200: ProjectUserSerializer(many=True)})
    def get(self, request):
        service = ProjectUserListService()
        project_user_list = service.get_projects_for_user(request.user)
        
        serializer = ProjectUserSerializer(project_user_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        