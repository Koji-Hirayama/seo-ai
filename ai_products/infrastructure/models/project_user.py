from django.db import models
from ai_products.models import User
from .project import Project
from ai_products.domain.project_user import ProjectUser as DomainProjectUser

class ProjectUser(models.Model):
     project = models.ForeignKey(Project, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     is_admin = models.BooleanField(default=True)
     
     def __str__(self) -> str:
          return self.project.name
     
     @classmethod
     def from_domain(cls, obj: DomainProjectUser) -> "ProjectUser":
          """ドメインモデルからのファクトリメソッド"""
          instance = cls(
               id=obj.id, 
               project=Project.from_domain(obj.project),
               user=User.from_domain(obj.user),
               is_admin=obj.is_admin,
          )
          return instance

     def to_domain(self) -> DomainProjectUser:
          """Djangoモデルからドメインモデルに変換するメソッド"""
          return DomainProjectUser(
               id=self.id,
               project=self.project.to_domain(),
               user=self.user.to_domain(),
               is_admin=self.is_admin
          )
     
     
     