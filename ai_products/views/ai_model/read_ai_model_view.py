from rest_framework.views import APIView
from ai_products.serializers.ai_model.ai_model_serializer import AiModelSerialiser
from ai_products.services.ai_model.get_ai_models_service import GetAiModelService
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


class GetAiModelsAPIView(APIView):

    @extend_schema(responses={200: AiModelSerialiser(many=True)})
    def get(self, request):
        service = GetAiModelService()
        ai_model_list = service.get_ai_models()

        serializer = AiModelSerialiser(ai_model_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
