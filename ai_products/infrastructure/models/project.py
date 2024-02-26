from typing import List
from django.db import models
from ai_products.models import User
from ai_products.domain.project import Project as DomainProject
from ai_products.domain.user import User as DomainUser
from typing import List

class Project(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through="ProjectUser", related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, )
    
    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def from_domain(cls, obj: DomainProject) -> "Project":
        """ドメインモデルからのファクトリメソッド"""
        instance = cls(
            id=obj.id, 
            name=obj.name, 
            created_at=obj.created_at,
            updated_at=obj.updated_at, 
            deleted_at=obj.deleted_at
        )
        # ManyToManyの場合の処理
        if obj.users is not None:
            instance.users.set([User.from_domain(user) for user in obj.users])
        return instance

    def to_domain(self) -> DomainProject:
        """Djangoモデルからドメインモデルに変換するメソッド"""
        # (仕様)ManyToManyのデフォルトはNone。(無限ループ防止)
        return DomainProject(
            id=self.id,
            name=self.name,
            users=None,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )
    
    def users_to_user_domain_list(self) -> List[DomainUser]:
        """ManyToManyのusersをドメインモデルに変換して返す(※プレフェッチ済み推奨)"""
        return [user.to_domain() for user in self.users.all()]
    
        