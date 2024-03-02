from django.db.models.query import QuerySet
from ai_products.models import User
from ai_products.models import ProjectUser

class ProjectUserListService():
    def get_projects_for_user(self, user: User) -> QuerySet[ProjectUser]:
        """指定されたユーザーに紐づくProjectUserのリストを取得し、それに紐づくプロジェクト情報を返す"""
        project_user_list = ProjectUser.objects.select_related('project').prefetch_related('project__users').filter(user__id=user.id)
        return project_user_list
    
    