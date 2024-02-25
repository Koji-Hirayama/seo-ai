from ai_products.domain.project import ProjectRepositoryInterface
from ai_products.domain.project import Project as DomainProject

class CreateProjectService():
    def __init__(self, project_repository: ProjectRepositoryInterface):
        self.project_repository = project_repository

    def create_project(self, name:str, user_id:int) -> DomainProject:
        """Projectの作成"""
        create_project = self.project_repository.save(name=name, user_id=user_id)
        return create_project
    
    