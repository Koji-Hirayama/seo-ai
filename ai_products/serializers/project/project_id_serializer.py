from typing import Any
from rest_framework import serializers
from utils.errors import RequestErrorSerializer


class RequestProjectIdSerializer(RequestErrorSerializer):
    project_id = serializers.IntegerField(min_value=1)

    def get_error(self) -> dict[str, Any]:
        self.set_message("バリデーションに失敗しました。")
        return super().get_error()
