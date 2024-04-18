import datetime
from ai_products.models import Prompt
from typing import Dict
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from ai_products.models import Work, User, AiModel
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class CreatePromptService:
    def create_prompt(
        self,
        prompt: str,
        output_example_model_description: str,
        output_example_model: Dict,
        work_id: int,
        ai_model_id: int,
        user: User,
        order: int,
        token: int,
        cost: float,
        total_cost: float,
        request_date: datetime.datetime,
    ) -> Prompt:
        try:
            work = Work.objects.get(id=work_id)
            ai_model = AiModel.objects.get(id=ai_model_id)
        except (Work.DoesNotExist, AiModel.DoesNotExist) as e:
            if isinstance(e, Work.DoesNotExist):
                error_detail: ErrorDetail = ErrorDetail(
                    field="work", message=f"id:{work_id}のWorkは存在しません。"
                )
            elif isinstance(e, AiModel.DoesNotExist):
                error_detail: ErrorDetail = ErrorDetail(
                    field="ai_model", message=f"id:{ai_model}のAiModelは存在しません。"
                )
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_ELEMENT_NOT_FOUND,
                message="Promptの作成に必要な要素が存在しません。",
                error_details=[error_detail],
            )
        try:
            create_prompt = self.create_prompt_direct(
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
        except CustomApiErrorException as e:
            raise e
        return create_prompt

    def create_prompt_direct(
        self,
        prompt: str,
        output_example_model_description: str,
        output_example_model: Dict,
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
