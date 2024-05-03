from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ai_products.serializers.work.create_work_serializer import (
    CreateWorkSerializer,
    RequestCreateWorkSerializer,
)
from ai_products.services.work.create_work_service import CreateWorkService
from ai_products.utils import IsRelatedToProjectUser
from drf_spectacular.utils import extend_schema
from utils.errors import ErrorType, CustomApiErrorException


class CreateWorkAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    @extend_schema(
        request=RequestCreateWorkSerializer, responses={200, CreateWorkSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = RequestCreateWorkSerializer(
            data=request.data, error_type=ErrorType.TASK_ID_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        task_id = serializer.validated_data.get("task_id")
        try:
            service = CreateWorkService()
            work = service.create_work(task_id=task_id)
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=status.HTTP_404_NOT_FOUND)
        serializer = CreateWorkSerializer(work)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
