from rest_framework.views import APIView
from ai_products.serializers import RequestScrapingSerializer, ScrapingSerialize
from ai_products.services import GetScrapingResultsService
from utils.errors import ErrorType
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


class ScrapingResultsAPIView(APIView):
    @extend_schema(
        request=RequestScrapingSerializer, responses={200: ScrapingSerialize(many=True)}
    )
    def post(self, request):
        serializer = RequestScrapingSerializer(
            data=request.data, error_type=ErrorType.SCRAPING_URL_BAD_REQUEST
        )
        if not serializer.is_valid():
            return Response(
                serializer.get_error(), status=serializer.get_error_http_status()
            )
        urls = serializer.validated_data.get("urls")
        service = GetScrapingResultsService()
        results = service.get_results(urls)
        serializer = ScrapingSerialize(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
