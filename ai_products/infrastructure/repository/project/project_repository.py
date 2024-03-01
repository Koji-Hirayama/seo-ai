from ai_products.domain.project import Project as DomainProject
from ai_products.domain.project import ProjectRepositoryInterface
from ai_products.infrastructure.models import Project

class ProjectRepository(ProjectRepositoryInterface):
    def save(self, project: DomainProject) -> DomainProject:
        # Projectの作成
        db_project = Project.from_domain(project)
        db_project.save()
        
        return db_project.to_domain()
    
    
    def get_project_with_tasks(self, id: int) -> DomainProject:
        db_project = Project.objects.prefetch_related('tasks').get(id=id)
        return db_project.to_domain()
        