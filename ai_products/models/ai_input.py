from django.db import models
from .ai_input_type import AiInputType


class AiInput(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_input_type = models.ForeignKey(
        AiInputType, on_delete=models.CASCADE, related_name="ai_inputs"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def get_ai_input_fields(self):
        return self.ai_input_fields

    def get_ai_input_field_by_field_type_id(self, ai_input_field_type_id: int):
        # ai_input_field_typeのidでフィルタリング
        input_fields = self.get_ai_input_fields().filter(
            ai_input_field_type__id=ai_input_field_type_id
        )
        # 最初のフィールドを返す、存在しない場合はNoneを返す
        return input_fields.first()
