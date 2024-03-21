from typing import List
from ai_products.models import Task, Project, User, AiType
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from utils.errors import ErrorType, CustomApiErrorException, ErrorDetail


class CreateTaskService:

    def create_task(
        self, user: User, project_id: int, ai_type_id: int, name: str, description: str
    ) -> Task:

        not_found_errors: List[ErrorDetail] = []

        # Projectの取得とエラーハンドリング
        # projectの存在確認&Userと関係してる場合取得
        project = Project.objects.filter(id=project_id, users__id=user.id).first()
        if project is None:
            not_found_errors.append(
                ErrorDetail(
                    field=ErrorType.PROJECT_NOT_FOUND.get_error_type(),
                    message=f"このユーザーに該当する、project_id:{project_id}のプロジェクトが存在しません。",
                )
            )
        # AiTypeの取得とエラーハンドリング
        ai_type = AiType.objects.filter(id=ai_type_id).first()
        if ai_type is None:
            not_found_errors.append(
                ErrorDetail(
                    field=ErrorType.AI_TYPE_NOT_FOUND.get_error_type(),
                    message=f"id:{ai_type_id}のAiTypeは存在しません・",
                )
            )

        if not_found_errors:
            # ProjectまたはAiTypeが存在しない場合の例外処理
            raise CustomApiErrorException(
                error_type=ErrorType.CREATE_TASK_NOT_FOUND,
                message="ProjectまたはAiTypeが存在しません。タスクの作成ができません。",
                error_details=not_found_errors,
            )

        # Taskの作成
        task = Task(
            name=name,
            description=description,
            project=project,
            ai_type=ai_type,
            user=user,
        )
        task.save()
        return task