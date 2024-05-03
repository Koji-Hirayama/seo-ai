from typing import Any
from rest_framework import serializers
from ai_products.models import Work
from utils.errors import RequestErrorSerializer


class RequestProjectIdAndTaskIdSerializer(RequestErrorSerializer):
    task_id = serializers.IntegerField(min_value=1)

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()


class GetWorksForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ("id", "version", "created_at", "updated_at")
