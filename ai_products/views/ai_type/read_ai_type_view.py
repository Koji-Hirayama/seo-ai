from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ai_products.serializers.ai_type.ai_types_serializer import AiTypeSerializer
from ai_products.services.ai_type.get_ai_types_service import GetAiTypesService


class GetAiTypesAPIView(APIView):

    @extend_schema(responses={200: AiTypeSerializer(many=True)})
    def get(self, request):
        service = GetAiTypesService()
        ai_type_list = service.get_ai_types()

        serializer = AiTypeSerializer(ai_type_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
