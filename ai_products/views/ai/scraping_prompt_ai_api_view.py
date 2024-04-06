from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ai_products.serializers import (
    AiResponseSerializer,
)
from ai_products.serializers.ai.logic.scraping_prompt_ai_serializer import (
    RequestScrapingPromptAiSerializer,
)
from ai_products.services.ai.core.ai_service import AiService
from ai_products.services.ai.logic.scraping_prompt_ai_service import (
    ScrapingPromptAiService,
)

from ai_products.utils import IsRelatedToProjectUser
from utils.errors import ErrorType
from rest_framework.response import Response
from rest_framework import status
from utils.errors import CustomApiErrorException


class ScrapingPromptAiAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    def post(self, request, *args, **kwargs):
        serializer = RequestScrapingPromptAiSerializer(
            data=request.data,
            error_type=ErrorType.PROMPT_BAD_REQUEST,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(
                serializer.get_error(), status=serializer.get_error_http_status()
            )

        url = serializer.validated_data.get("url")
        input = serializer.validated_data.get("input")
        description = serializer.validated_data.get("output_example_model_description")
        output_example_model = serializer.get_output_example_model()
        output_model_class = serializer.get_output_model_class()

        ai_service = AiService(
            ScrapingPromptAiService(
                urls=[url],
                input=input,
                output_example_model=output_example_model,
                output_example_model_description=description,
                output_model_class=output_model_class,
            )
        )
        try:
            result = ai_service.save_ai_answer(
                work_id=1, llm_id=1, user=request.user, order=1
            )
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=e.get_error_http_status())
        serializer = AiResponseSerializer(result.prompt_output)
        return Response(serializer.data, status=status.HTTP_200_OK)
