from typing import List
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import ValidationError

from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class SimpleLlmAnswerWithFunctionCalling:

    def llm_answer_with_model(
        self,
        messages: List[any],
        output_example_model_description: str,
        output_model_class: BaseModel,
    ) -> BaseModel:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0, n=1)
        function = {
            "name": "answer_to_prompt",
            "description": output_example_model_description,
            "parameters": output_model_class.model_json_schema(),
        }
        try:
            response = llm.predict_messages(
                messages=messages,
                functions=[function],
                function_call={"name": function["name"]},
            )
        except Exception:
            raise CustomApiErrorException(
                error_type=ErrorType.OPENAI_REQUEST_INTERNAL_SERVER_ERROR,
                message="OpenAIのサーバー側で問題が発生しました。",
            )

        try:
            arguments = response.additional_kwargs["function_call"]["arguments"]
            print(type(arguments))
            output_model = output_model_class.model_validate_json(arguments)
        except ValidationError as e:
            # バリデーションエラー時の処理
            error_details: List[ErrorDetail] = []
            # エラーの詳細を取得して表示
            for error in e.errors():
                error_detail: ErrorDetail = ErrorDetail(
                    field=error["type"], message=error["msg"]
                )
                error_details.append(error_detail)
            # 必要に応じてさらにエラー処理を行う
            raise CustomApiErrorException(
                error_type=ErrorType.AI_MODEL_VALIDATE_JSON_BAD_REQUEST,
                message="AIの回答をModelに変換できませんでした。",
                error_details=error_details,
            )
        except KeyError as e:
            # KeyErrorが発生した場合の処理
            missing_key = e.args[0]
            error_detail: ErrorDetail = ErrorDetail(
                field=missing_key, message=f"'{missing_key}'キーが存在しません。"
            )
            raise CustomApiErrorException(
                error_type=ErrorType.AI_MODEL_VALIDATE_JSON_BAD_REQUEST,
                message="AIの回答を取得するためのKeyが存在しません。",
                error_details=[error_detail],
            )
        return output_model
