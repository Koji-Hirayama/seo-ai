from pydantic import BaseModel
from pydantic import ValidationError
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail
from typing import Dict, List


class AiOutputConverterService:
    def function_call_arguments_to_dict(
        self, additional_kwargs: any, output_model_class: BaseModel
    ) -> Dict:
        """_summary_:
            FunctionCalling結果の引数をDictに変換して取得。
            ※functionが実行されなかった場合は、エラーを返す。
        Args:
            additional_kwargs (any): FunctionCalling結果のadditional_kwargsを指定
            output_model_class (BaseModel): 期待するモデルクラスを指定

        Returns:
            Dict: FunctionCalling結果の引数をDictに変換して返す
        """
        try:
            arguments = additional_kwargs["function_call"]["arguments"]
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
                message="ValidationError: AI出力のjsonが正しくありません。",
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
                message="KeyError: AIがfunctionを実行しませんでした。",
                error_details=[error_detail],
            )
        return output_model.model_dump()
