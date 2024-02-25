from ai_products.domain.project_user import ProjectUserRepositoryInterface
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserList
from ai_products.infrastructure.models import ProjectUser

class ProjectUserRepository(ProjectUserRepositoryInterface):
    
    def get_project_user_list_by_user_id(self, user_id: int) -> DomainProjectUserList:
        db_project_user_list = ProjectUser.objects.select_related('user', 'project').prefetch_related('project__users').filter(user__id=user_id)
        project_user_list = [data.to_domain() for data in db_project_user_list]
        return DomainProjectUserList(project_user_list=project_user_list)
