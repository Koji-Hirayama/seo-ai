from rest_framework.views import APIView
from ai_products.serializers import (
    GetAiTypeInputFieldsSerializer,
    RequestAiTypeInputFieldsSerializer,
)
from ai_products.services import GetAiTypeInputFieldsService
from utils.errors import ErrorType, CustomApiErrorException
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from ai_products.utils import IsRelatedToProjectUser


class GetAiTypeInputFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ai_type_id",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: GetAiTypeInputFieldsSerializer(many=True)},
    )
    def get(self, request, *args, **kwargsst):
        serializer = RequestAiTypeInputFieldsSerializer(
            data=request.query_params,
            error_type=ErrorType.AI_TYPE_BAD_REQUEST,
        )
        if not serializer.is_valid():
            return Response(
                serializer.get_error(), status=serializer.get_error_http_status()
            )
        ai_type_id = serializer.validated_data.get("ai_type_id")
        try:
            service = GetAiTypeInputFieldsService()
            input_fields = service.get_ai_type_input_fields(ai_type_id)
        except CustomApiErrorException as e:
            return Response(e.get_error(), status=e.get_error_http_status())
        serializer = GetAiTypeInputFieldsSerializer(input_fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
