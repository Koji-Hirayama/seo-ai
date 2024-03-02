from django.db import models
from ai_products.models.user import User
from .project import Project

class ProjectUser(models.Model):
     project = models.ForeignKey(Project, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     is_admin = models.BooleanField(default=True)
     
     def __str__(self) -> str:
          return self.project.name
     

     
