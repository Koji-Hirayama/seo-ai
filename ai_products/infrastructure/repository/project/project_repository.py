from ai_products.domain.project import Project as DomainProject
from ai_products.domain.project import ProjectRepositoryInterface
from ai_products.models import User
from ai_products.infrastructure.models import ProjectUser, Project

class ProjectRepository(ProjectRepositoryInterface):
    def save(self, name:str, user_id:int) -> DomainProject:
        # Projectの作成
        db_project = Project(name=name)
        db_project.save()
        # ProjectとUserの紐付け
        user = User(id=user_id)
        db_project_user = ProjectUser(project=db_project, user=user, is_admin=True)
        db_project_user.save()
        
        return db_project.to_domain()
