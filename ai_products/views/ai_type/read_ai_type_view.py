from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ai_products.serializers import AiTypeSerializer
from ai_products.services import GetAiTypesService
from drf_spectacular.utils import extend_schema


class GetAiTypesAPIView(APIView):

    @extend_schema(responses={200: AiTypeSerializer(many=True)})
    def get(self, request):
        service = GetAiTypesService()
        ai_type_list = service.get_ai_types()

        serializer = AiTypeSerializer(ai_type_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
