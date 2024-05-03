from rest_framework.views import APIView
from ai_products.serializers import RequestTaskAiSerializer
from ai_products.services import AiService
from ai_products.services import TaskAiService
from ai_products.services.ai.core.ai_service import AiAnswerResults
from ai_products.utils import IsRelatedToProjectUser
from rest_framework.permissions import IsAuthenticated
from utils.errors import CustomApiErrorException, ErrorType
from rest_framework.response import Response
from ai_products.serializers import (
    AiResponseSerializer,
)
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
        # ai_type_id = serializer.validated_data.get("ai_type_id")
        # ai_model_id = serializer.validated_data.get("ai_model_id")
        # task_id = serializer.validated_data.get("task_id")
        # urls = serializer.validated_data.get("urls")
        # prompt_input = serializer.validated_data.get("prompt_input")
        # description = serializer.validated_data.get("output_example_model_description")
        # output_example_model = serializer.get_output_example_model()
        # output_model_class = serializer.get_output_model_class()

        # test = serializer.get_ai_request_params()
        # return Response(
        #     {
        #         "ai_type_id": test.ai_type_id,
        #         "ai_model_id": test.ai_model_id,
        #         "urls": test.urls,
        #         "prompt_input": test.prompt_input,
        #         "description": test.output_example_model_description,
        #         "output_example_model": test.output_example_model.model_dump_json(),
        #         "output_model_class": test.output_example_model.model_json_schema(),
        #     },
        #     status=status.HTTP_200_OK,
        # )
        ai_request_params = serializer.get_ai_request_params()
        ai_service = AiService(
            params=ai_request_params,
            ai_service=TaskAiService(),
        )
        try:
            result: AiAnswerResults = ai_service.save_ai_answer(
                task_id=ai_request_params.task_id, user=request.user
            )
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=e.get_error_http_status())

        serializer = AiResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
