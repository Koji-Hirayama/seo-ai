from typing import List
from langchain_openai import ChatOpenAI
from ai_products.models import AiModel
from utils.errors import OpenAIErrorHandler
from langchain.schema import HumanMessage
import json
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class ChatOpenAi:
    def __init__(self, ai_model: AiModel, temperature: int = 0, n: int = 1):
        self.ai_model = ai_model
        self.temperature = temperature
        self.n = n
        self.chat_open_ai = ChatOpenAI(
            model_name=self.ai_model.name, temperature=self.temperature, n=self.n
        )

    def function_call_predict_messages(
        self, messages: List[any], functions: List[any], min_output_token=1000
    ):
        """_summary_

        Args:
            messages (List[any]): メッセージ
            functions (List[any]): 関数リスト
            min_output_token (int, optional): 出力トークン数の確保. Defaults to 1000.

        """
        if not self.is_token_limit_validation(messages, functions, min_output_token):
            # トークン上限の事前チェック
            error_details = [
                ErrorDetail(field="model", message=self.ai_model.name),
                ErrorDetail(
                    field="prompt_token",
                    message=str(self.get_num_tokens_from_messages(messages, functions)),
                ),
                ErrorDetail(
                    field="prompt_token_limit",
                    message=str(self.ai_model.token_limit - min_output_token),
                ),
            ]
            raise CustomApiErrorException(
                error_type=ErrorType.AI_MODEL_RECOMMENDED_PROMPT_TOKEN_LIMIT_BAD_REQUEST,
                message="プロンプトのトークン数が推奨する上限数を超えています。",
                error_details=error_details,
            )

        try:
            # llmリクエスト
            result = self.chat_open_ai.predict_messages(
                messages=messages,
                functions=functions,
            )
        except Exception as e:
            raise OpenAIErrorHandler.handle_error(e)
        return result

    def get_num_tokens_from_messages(
        self, messages: List[any], functions: List[any] = []
    ):
        """トークン数取得"""
        _messages = messages.copy()
        _messages.append(HumanMessage(content=json.dumps(functions)))
        prompt_token_size = self.chat_open_ai.get_num_tokens_from_messages(
            messages=_messages
        )
        return prompt_token_size

    def is_token_limit_validation(
        self,
        messages: List[any],
        functions: List[any] = [],
        min_output_token: int = 1000,
    ):
        """トークン数の上限チェック"""
        prompt_token_limit = self.ai_model.token_limit - min_output_token
        if self.get_num_tokens_from_messages(messages, functions) <= prompt_token_limit:
            return True
        return False
