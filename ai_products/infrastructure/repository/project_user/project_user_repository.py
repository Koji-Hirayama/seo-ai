from ai_products.domain.project_user import ProjectUserRepositoryInterface
from ai_products.domain.project_user import ProjectUserList as DomainProjectUserList
from ai_products.domain.project_user import ProjectUser as DomainProjectUser
from ai_products.domain.user import User as DomainUser
from ai_products.infrastructure.models import ProjectUser

class ProjectUserRepository(ProjectUserRepositoryInterface):
    
    def get_project_user_list_by_user(self, user: DomainUser) -> DomainProjectUserList:
        # 必要なデータセットをプレフェッチして用意
        db_project_user_list = ProjectUser.objects.select_related('user', 'project').prefetch_related('project__users').filter(user__id=user.id)
        # ProjectUserのドメインリスト取得
        project_user_list = [data.to_domain() for data in db_project_user_list]
        # ManyToMany(多対多)のフィールドを外部注入
        for index, item in enumerate(project_user_list):
            item.project.add_users(db_project_user_list[index].project.users_to_user_domain_list())
        
        return DomainProjectUserList(project_user_list=project_user_list)


    def save(self, project_user: DomainProjectUser) -> DomainProjectUser:
        db_project_user = ProjectUser.from_domain(project_user)
        db_project_user.save()
        return db_project_user.to_domain()