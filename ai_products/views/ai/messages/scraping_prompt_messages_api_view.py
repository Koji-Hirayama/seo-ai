from rest_framework.views import APIView
from ai_products.serializers import (
    RequestScrapingPromptMessageSeriaizer,
    ScrapingPromptMessageSeriaizer,
)
from utils.errors import ErrorType
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ai_products.services import GetScrapingPromptMessage


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
        service = GetScrapingPromptMessage()
        message = service.get_human_message(input, urls)
        serializer = ScrapingPromptMessageSeriaizer({"prompt": message.content})
        return Response(serializer.data, status=status.HTTP_200_OK)
