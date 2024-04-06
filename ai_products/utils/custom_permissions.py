from rest_framework.permissions import BasePermission
from ai_products.models import ProjectUser
from utils.errors import CustomApiException, ErrorType, ErrorDetail

# ===================================================
# カスタムパーミッションに関しては、必ずパスパラメータから取得するようにする。
# ===================================================


# Userとプロジェクトの関係パーミッション
class IsRelatedToProjectUser(BasePermission):
    """
    ユーザーがプロジェクトに紐づいているかどうかをチェックするカスタムパーミッションクラス。
    """

    def has_permission(self, request, view):

        # パスパラメータからproject_id を取得
        project_id = view.kwargs.get("project_id")

        if not project_id:
            raise CustomApiException(
                error_type=ErrorType.PROJECT_USER_FORBIDDEN,
                message="プロジェクトの権限がありません。",
                error_details=[
                    ErrorDetail(
                        field="project_id", message="project_idが確認できません。"
                    )
                ],
            )

        # ユーザーとプロジェクトの関連をチェック
        if not ProjectUser.objects.filter(
            project_id=project_id, user=request.user
        ).exists():
            raise CustomApiException(
                error_type=ErrorType.PROJECT_USER_FORBIDDEN,
                message="プロジェクトの権限がありません。",
            )
        return True
