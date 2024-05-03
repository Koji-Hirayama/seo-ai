from typing import List, Dict
from openai import BaseModel
from rest_framework.views import APIView
from ai_products.models import PromptOutput
from ai_products.serializers.ai.utils.ai_serializer import (
    AiResponseSerializer,
    BaseRequestPromptSerializer,
)
from ai_products.serializers.ai.utils.dynamic_pydantic_model_serializer import (
    AiOutputPydanticModelSerialiser,
)
from ai_products.services.ai.core.ai_service import AiService
from ai_products.services.prompt.create_prompt_service import CreatePromptService
from ai_products.services.prompt_output.create_prompt_output_service import (
    CreatePromptOutputService,
)
from utils.errors import ErrorType
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ai_products.utils import IsRelatedToProjectUser


class AiResponseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToProjectUser]

    def post(self, request, *args, **kwargs):
        serializer = BaseRequestPromptSerializer(
            data=request.data,
            error_type=ErrorType.PROMPT_BAD_REQUEST,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.get_error(), status=status.HTTP_400_BAD_REQUEST)

        url = serializer.validated_data.get("url")
        input = serializer.validated_data.get("input")
        output_example_model_description = serializer.validated_data.get(
            "output_example_model_description"
        )
        output_example_model = serializer.validated_data.get("output_example_model")

        dynamicPydanticModel = AiOutputPydanticModelSerialiser()
        output_example_model = dynamicPydanticModel.create_model(output_example_model)

        ai_service = AiService()
        # result = ai_service.chat()
        result = ai_service.test_ai(
            url, input, output_example_model_description, output_example_model
        )
        promptOutput = PromptOutput(
            id=1, output="", output_json=result, prompt_id=1, ai_model_id=1
        )

        prompt_service = CreatePromptService()
        prompt_output_service = CreatePromptOutputService()

        serializer = AiResponseSerializer(promptOutput)
        return Response(serializer.data, status=status.HTTP_200_OK)


# question_type_id毎の入力欄が出来上がる
class Question(BaseModel):
    id: int
    question: str
    example: str
    question_type_id: int


# ====================================
# question_type毎の想定
# ====================================
# シンプルな質問の回答
class QuestionType1(BaseModel):
    input: str


# スクレイピングのURLとスクレイピングに対して何をしたかの解答
class QuestionType2(BaseModel):
    urls: List[str]
    input: str


# Google検索キーワード
class QuestionType3(BaseModel):
    keyword: str


class QuestionAnswer(BaseModel):
    id: int
    question_id: str
    answer: Dict


# ====================================

# class TemplateQA:


# class Contents(BaseModel):
#     questions: str
#     content: str
