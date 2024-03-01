from django.db import models
from ai_products.domain.ai_type import AiType as DomainAiType

class AiType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def from_domain(cls, obj: DomainAiType) -> "AiType":
        """ドメインモデルからのファクトリメソッド"""
        instance = cls(
            id=obj.id, 
            name=obj.name, 
            description=obj.description,
            created_at=obj.created_at,
        )
        return instance

    def to_domain(self) -> DomainAiType:
        """Djangoモデルからドメインモデルに変換するメソッド"""
        # (仕様)ManyToManyのデフォルトはNone。(無限ループ防止)
        return DomainAiType(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
        ) 