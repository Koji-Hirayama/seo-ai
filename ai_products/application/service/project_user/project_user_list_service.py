from ai_products.domain.project_user import ProjectUserRepositoryInterface
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserList

class ProjectUserListService():
    def __init__(self, project_user_repository: ProjectUserRepositoryInterface):
        self.project_user_repository = project_user_repository
    
    def get_projects_for_user(self, user_id: int) -> DomainProjectUserList:
        """指定されたユーザーIDに紐づくProjectUserのリストを取得し、それに紐づくプロジェクト情報を返す"""
        project_user_list = self.project_user_repository.get_project_user_list_by_user_id(user_id)
        return project_user_list
    
    