from ai_products.models import ProjectUser
from ai_products.models import Project
from ai_products.models import User
from django.db import transaction

class CreateProjectService():
    
    def create_project(self, user: User, project_name: str) -> Project:
        """Projectの作成"""
        with transaction.atomic():
            project = Project(name=project_name)
            project.save()
            ProjectUser.objects.create(project=project, user=user, is_admin=True)
            return project
    
    