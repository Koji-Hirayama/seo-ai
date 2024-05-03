from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.serializers.project.create_project_serializer import (
    CreateProjectSerializer,
    RequestCreateProjectSerializer,
)
from drf_spectacular.utils import extend_schema
from ai_products.services.project.create_project_service import CreateProjectService
from utils.errors import ErrorType


class CreateProjectAPIView(APIView):

    @extend_schema(
        request=RequestCreateProjectSerializer, responses={201: CreateProjectSerializer}
    )
    def post(self, request):
        serializer = RequestCreateProjectSerializer(
            data=request.data, error_type=ErrorType.CREATE_PROJECT_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        project_name = serializer.validated_data.get("name")
        service = CreateProjectService()
        project_user = service.create_project(
            user=request.user, project_name=project_name
        )
        serializer = CreateProjectSerializer(project_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
