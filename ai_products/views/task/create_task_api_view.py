from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ai_products.serializers import RequestCreateTaskSerializer, CreateTaskSerializer
from ai_products.services import CreateTaskService
from utils.errors import ErrorType, CustomApiErrorException


class CreateTaskApiView(APIView):

    @extend_schema(
        request=RequestCreateTaskSerializer, responses={201: CreateTaskSerializer}
    )
    def post(self, request):
        serializer = RequestCreateTaskSerializer(
            data=request.data, error_type=ErrorType.CREATE_TASK_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        task_name = serializer.validated_data.get("name")
        task_description = serializer.validated_data.get("description")
        project_id = serializer.validated_data.get("project_id")
        ai_type_id = serializer.validated_data.get("ai_type_id")
        try:
            service = CreateTaskService()
            task = service.create_task(
                name=task_name,
                description=task_description,
                project_id=project_id,
                ai_type_id=ai_type_id,
                user=request.user,
            )
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=status.HTTP_404_NOT_FOUND)
        serializer = CreateTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
