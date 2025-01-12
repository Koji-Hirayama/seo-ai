import datetime
from ai_products.models import Prompt
from typing import Dict
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from ai_products.models import Work, User, AiModel, AiRequest
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class CreatePromptService:
    # 外部キーのデータを外から注入して保存
    def create_prompt(
        self,
        prompt: str,
        output_example_model_description: str,
        output_example_model: Dict,
        ai_request: AiRequest,
        work: Work,
        ai_model: AiModel,
        user: User,
        order: int,
        token: int,
        cost: float,
        total_cost: float,
        request_date: datetime.datetime,
    ) -> Prompt:
        try:
            create_prompt = Prompt(
                ai_request=ai_request,
                prompt=prompt,
                output_example_model_description=output_example_model_description,
                output_example_model=output_example_model,
                work=work,
                ai_model=ai_model,
                user=user,
                order=order,
                token=token,
                cost=cost,
                total_cost=total_cost,
                request_date=request_date,
            )
            # full_cleanを呼び出してモデルのバリデーションを実行
            create_prompt.full_clean()
            # モデルインスタンスをデータベースに保存
            create_prompt.save()
        except ValidationError as e:
            # バリデーションエラーのハンドリング
            error_detail: ErrorDetail = ErrorDetail(
                field="prompt", message="バリデーションエラーが発生しました。"
            )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_BAD_REQUEST,
                message="Promptの作成に失敗しました。",
                error_details=[error_detail],
            )
        except DatabaseError as e:
            # データベースエラーのハンドリング
            error_detail: ErrorDetail = ErrorDetail(
                field="prompt", message="データベースエラーが発生しました。"
            )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_INTERNAL_SERVER_ERROR,
                message="Promptの作成に失敗しました。",
                error_details=[error_detail],
            )
        return create_prompt
