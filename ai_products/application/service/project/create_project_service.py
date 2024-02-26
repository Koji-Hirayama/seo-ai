from ai_products.domain.project import ProjectRepositoryInterface
from ai_products.domain.project_user import ProjectUserRepositoryInterface
from ai_products.domain.project import Project as DomainProject
from ai_products.domain.project_user import ProjectUser as DomainProjectUser
from ai_products.domain.user import User as DomainUser
from django.db import transaction

class CreateProjectService():
    def __init__(self, project_repository: ProjectRepositoryInterface, project_user_repository: ProjectUserRepositoryInterface):
        self.project_repository = project_repository
        self.project_user_repository = project_user_repository

    def create_project(self, user: DomainUser, project: DomainProject) -> DomainProject:
        """Projectの作成"""
        with transaction.atomic():
            project = self.project_repository.save(project)
            project_user = DomainProjectUser(project=project, user=user, is_admin=True)
            self.project_user_repository.save(project_user)
            return project
    
    