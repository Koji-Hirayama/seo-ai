from django.db import models
from ai_products.models import User
from .ai_type import AiType
from .project import Project
from ai_products.domain.task import Task as DomainTask



class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_type = models.ForeignKey(AiType, on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    @classmethod
    def from_domain(cls, obj: DomainTask) -> "Task":
        """ドメインモデルからのファクトリメソッド"""
        instance = cls(
            id=obj.id, 
            name=obj.name, 
            description=obj.description,
            ai_type=obj.ai_type,
            project=obj.project,
            user=obj.user,
            created_at=obj.created_at,
            updated_at=obj.updated_at, 
            deleted_at=obj.deleted_at
        )
        return instance
    
    def to_domain(self) -> DomainTask:
        """Djangoモデルからドメインモデルに変換するメソッド"""
        # (仕様)ManyToManyのデフォルトはNone。(無限ループ防止)
        return DomainTask(
            id=self.id,
            name=self.name,
            description=self.description,
            ai_type=self.ai_type.to_domain(),
            project=self.project.to_domain(),
            user=self.user.to_domain(),
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        ) 
    