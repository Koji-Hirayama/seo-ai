from ai_products.models import PromptInput
from typing import List
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail
from django.db import IntegrityError, transaction


class CreatePromptInputService:

    def create_prompt_inputs(self, prompt_inputs: List[PromptInput]):
        try:
            with transaction.atomic():
                # bulk_createを使用してリストのオブジェクトをDBに保存
                PromptInput.objects.bulk_create(prompt_inputs)
        except IntegrityError as e:
            # IntegrityErrorは、外部キー制約違反やその他のデータベース制約に関連するエラーを捕捉します
            print(f"Error during saving PromptInputs: {e}")
            # 必要に応じてさらにエラーハンドリングをここに追加するか、エラーを再発生させる
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_INPUTS_NOT_FOUND, message=str(e)
            )
        except ValueError as e:
            print(f"Value error: {e}")
            # エラー処理をここに書く
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_PROMPT_INPUTS_NOT_FOUND, message=str(e)
            )
