from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ai_products.serializers.work.get_works_for_task_serializer import (
    GetWorksForTaskSerializer,
    RequestProjectIdAndTaskIdSerializer,
)
from ai_products.services.work.get_works_for_task_service import GetWorksForTaskService
from utils.errors import ErrorType
from utils.errors import CustomApiErrorException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from ai_products.utils import IsRelatedToProjectUser


class GetWorksForTaskAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="task_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: GetWorksForTaskSerializer},
    )
    def get(self, request, *args, **kwargs):
        serializer = RequestProjectIdAndTaskIdSerializer(
            data=request.query_params,
            error_type=ErrorType.PROJECT_ID_AND_TASK_ID_BAD_REQUEST,
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        task_id = serializer.validated_data.get("task_id")
        try:
            service = GetWorksForTaskService()
            works = service.get_works_for_task(task_id=task_id)
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=status.HTTP_404_NOT_FOUND)

        serializer = GetWorksForTaskSerializer(works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
