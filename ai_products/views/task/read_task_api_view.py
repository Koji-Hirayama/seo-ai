from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ai_products.serializers import RequestIdSerializer
from rest_framework import status
from ai_products.serializers import GetTaskForProjectSerializer
from ai_products.serializers import RequestProjectIdSerializer
from ai_products.services import GetTasksForProjectService
from utils.errors import ErrorType, CustomApiErrorException


class GetTasksForProjectAPIView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="project_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={200: GetTaskForProjectSerializer},
    )
    def get(self, request):
        # クエリパラメータからidを取得
        serializer = RequestProjectIdSerializer(
            data=request.query_params, error_type=ErrorType.PROJECT_ID_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        project_id = serializer.validated_data.get("project_id")
        try:
            service = GetTasksForProjectService()
            project_tasks = service.get_tasks_for_project(project_id)
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=status.HTTP_404_NOT_FOUND)

        serializer = GetTaskForProjectSerializer(project_tasks)
        return Response(serializer.data, status=status.HTTP_200_OK)
