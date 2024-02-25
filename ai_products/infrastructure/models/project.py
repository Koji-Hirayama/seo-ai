from django.db import models
from ai_products.models import User
from ai_products.domain.project import Project as DomainProject

class Project(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through="ProjectUser", related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, )
    
    def __str__(self) -> str:
        return self.name
    

    def to_domain(self) -> DomainProject:
        """Djangoモデルからドメインモデルに変換するメソッド"""
        return DomainProject(
            id=self.id,
            name=self.name,
            users=[user.to_domain() for user in self.users.all()],
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )