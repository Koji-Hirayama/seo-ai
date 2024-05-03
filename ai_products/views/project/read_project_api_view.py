from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.serializers.project.get_projects_for_user_serializer import (
    GetProjectsForUserSerializer,
)
from drf_spectacular.utils import extend_schema

from ai_products.services.project.get_projects_for_user_service import (
    GetProjectsForUserService,
)


class GetProjectsForUserAPIView(APIView):

    @extend_schema(responses={200: GetProjectsForUserSerializer(many=True)})
    def get(self, request):
        service = GetProjectsForUserService()
        project_user_list = service.get_projects_for_user(request.user)

        serializer = GetProjectsForUserSerializer(project_user_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
