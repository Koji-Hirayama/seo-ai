import datetime
from ai_products.models import PromptOutput
from typing import Dict
from ai_products.models import User, Prompt
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail
from django.core.exceptions import ValidationError
from django.db import DatabaseError


class CreatePromptOutputService:

    def create_prompt_output(
        self,
        output: str,
        output_model: Dict,
        prompt: Prompt,
        user: User,
        order: int,
        token: int,
        cost: float,
        total_cost: float,
        response_date: datetime.datetime,
        is_error: bool,
    ) -> PromptOutput:
        try:
            create_prompt_output = PromptOutput(
                output=output,
                output_model=output_model,
                prompt=prompt,
                work=prompt.work,
                ai_model=prompt.ai_model,
                user=user,
                order=order,
                token=token,
                cost=cost,
                total_cost=total_cost,
                response_date=response_date,
                is_error=is_error,
            )
            # full_cleanを呼び出してモデルのバリデーションを実行
            create_prompt_output.full_clean()
            # モデルインスタンスをデータベースに保存
            create_prompt_output.save()
        except ValidationError as e:
            # バリデーションエラーのハンドリング
            error_detail: ErrorDetail = ErrorDetail(
                field="prompt_output", message="バリデーションエラーが発生しました。"
            )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_OUTPUT_BAD_REQUEST,
                message="PromptOutputの作成に失敗しました。",
                error_details=[error_detail],
            )
        except DatabaseError as e:
            # データベースエラーのハンドリング
            error_detail: ErrorDetail = ErrorDetail(
                field="prompt_output", message="データベースエラーが発生しました。"
            )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_OUTPUT_INTERNAL_SERVER_ERROR,
                message="PromptOutputの作成に失敗しました。",
                error_details=[error_detail],
            )
        return create_prompt_output
