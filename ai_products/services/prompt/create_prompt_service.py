import datetime
from ai_products.models import Prompt
from typing import Dict
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from ai_products.models import Work, Llm, User
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class CreatePromptService:
    def create_prompt(
        self,
        prompt: str,
        output_example_model_description: str,
        output_example_model: Dict,
        work_id: int,
        llm_id: int,
        user: User,
        order: int,
        token: int,
        cost: float,
        total_cost: float,
        request_date: datetime.datetime,
    ) -> Prompt:
        try:
            work = Work.objects.get(id=work_id)
            llm = Llm.objects.get(id=llm_id)
        except (Work.DoesNotExist, Llm.DoesNotExist) as e:
            if isinstance(e, Work.DoesNotExist):
                error_detail: ErrorDetail = ErrorDetail(
                    field="work", message=f"id:{work_id}のWorkは存在しません。"
                )
            elif isinstance(e, Llm.DoesNotExist):
                error_detail: ErrorDetail = ErrorDetail(
                    field="llm", message=f"id:{llm_id}のLlmは存在しません。"
                )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_AI_PROMPT_TRANSACTION,
                message="Promptの作成に必要な要素が存在しません。",
                error_details=[error_detail],
            )
        try:
            create_prompt = Prompt(
                prompt=prompt,
                output_example_model_description=output_example_model_description,
                output_example_model=output_example_model,
                work=work,
                llm=llm,
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
                error_type=ErrorType.CREATE_AI_PROMPT_TRANSACTION,
                message="Promptの作成に失敗しました。",
                error_details=[error_detail],
            )
        except DatabaseError as e:
            # データベースエラーのハンドリング
            error_detail: ErrorDetail = ErrorDetail(
                field="prompt", message="データベースエラーが発生しました。"
            )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_AI_PROMPT_TRANSACTION,
                message="Promptの作成に失敗しました。",
                error_details=[error_detail],
            )
        return create_prompt
