from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from ai_products.serializers import GetTasksForProjectSerializer
from ai_products.serializers import RequestProjectIdSerializer
from ai_products.services import GetTasksForProjectService
from utils.errors import ErrorType, CustomApiErrorException
from rest_framework.permissions import IsAuthenticated
from ai_products.utils import IsRelatedToProjectUser


class GetTasksForProjectAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="project_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={200: GetTasksForProjectSerializer},
    )
    def get(self, request, *args, **kwargs):
        # クエリパラメータからidを取得
        serializer = RequestProjectIdSerializer(
            data=request.query_params, error_type=ErrorType.PROJECT_ID_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        project_id = serializer.validated_data.get("project_id")
        try:
            service = GetTasksForProjectService()
            tasks = service.get_tasks_for_project(project_id)
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=status.HTTP_404_NOT_FOUND)

        serializer = GetTasksForProjectSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
