from django.db import models
from .project import Project
from .user_api_key import UserApikey

class ProjectApikey(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_apikeys")
    user_apikey = models.ForeignKey(UserApikey, on_delete=models.CASCADE, related_name="project_apikeys")
    created_at = models.DateTimeField(auto_now_add=True)
    