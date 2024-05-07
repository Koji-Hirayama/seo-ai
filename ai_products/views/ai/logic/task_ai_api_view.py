from rest_framework.views import APIView
from ai_products.domains.ai.ai_request_params import AiRequestParams
from ai_products.serializers.ai.logic.task_ai_serializer import RequestTaskAiSerializer
from ai_products.serializers.ai.utils.ai_serializer import AiResponseSerializer
from ai_products.services.ai.core.ai_service import AiAnswerResults, AiService
from ai_products.services.ai.core.task_ai_service import TaskAiService
from ai_products.utils import IsRelatedToProjectUser
from rest_framework.permissions import IsAuthenticated
from utils.errors import CustomApiErrorException, ErrorType
from rest_framework.response import Response
from rest_framework import status


class TaskAiAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    def post(self, request, *args, **kwargs):
        serializer = RequestTaskAiSerializer(
            data=request.data,
            error_type=ErrorType.PROMPT_BAD_REQUEST,
        )
        if not serializer.is_valid():
            return Response(
                serializer.get_error(), status=serializer.get_error_http_status()
            )

        ai_request_params: AiRequestParams = serializer.get_ai_request_params()

        ai_service = AiService(
            params=ai_request_params,
            ai_service=TaskAiService(),
        )
        try:
            result: AiAnswerResults = ai_service.save_ai_answer(user=request.user)
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=e.get_error_http_status())

        serializer = AiResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
