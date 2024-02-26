from ai_products.domain.project_user import ProjectUserRepositoryInterface
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserList
from ai_products.domain.user import User as DomainUser

class ProjectUserListService():
    def __init__(self, project_user_repository: ProjectUserRepositoryInterface):
        self.project_user_repository = project_user_repository
    
    def get_projects_for_user(self, user: DomainUser) -> DomainProjectUserList:
        """指定されたユーザーに紐づくProjectUserのリストを取得し、それに紐づくプロジェクト情報を返す"""
        project_user_list = self.project_user_repository.get_project_user_list_by_user(user)
        return project_user_list
    
    