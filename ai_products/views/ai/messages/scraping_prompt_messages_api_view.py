from rest_framework.views import APIView
from ai_products.serializers import (
    RequestScrapingPromptMessageSeriaizer,
    ScrapingPromptMessageSeriaizer,
)
from ai_products.services import GetAiInputFieldService, GetScrapingResultsService
from utils.errors import ErrorType
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ai_products.services import GetScrapingPromptMessageService


class ScrapingPromptMessagesAPIView(APIView):
    @extend_schema(
        request=RequestScrapingPromptMessageSeriaizer,
        responses={200: ScrapingPromptMessageSeriaizer()},
    )
    def post(self, request):
        serializer = RequestScrapingPromptMessageSeriaizer(
            data=request.data, error_type=ErrorType.SCRAPING_PROMPT_MESSAGE_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(
                serializer.get_error(), status=serializer.get_error_http_status()
            )
        input = serializer.validated_data.get("input")
        urls = serializer.validated_data.get("urls")
        ai_input_field_id = serializer.validated_data.get("ai_input_field_id")
        get_ai_input_field_service = GetAiInputFieldService()
        ai_input_field = get_ai_input_field_service.get_ai_input_field(
            id=ai_input_field_id
        )
        message_service = GetScrapingPromptMessageService(
            context_input_field=ai_input_field, input=input
        )
        scraping_service = GetScrapingResultsService()
        scraping_results = scraping_service.get_results(urls=urls)
        message = message_service.get_scraping_result_injection_message(
            scraping_results=scraping_results
        )
        serializer = ScrapingPromptMessageSeriaizer({"prompt": message})
        return Response(serializer.data, status=status.HTTP_200_OK)
