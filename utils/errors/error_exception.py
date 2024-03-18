from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import BaseModel
from ..errors import ErrorType
from rest_framework import serializers


class ErrorDetail(BaseModel):
    field: str
    message: str


class _Error(BaseModel):
    status: int
    error: str
    error_type: str
    message: str
    code: str
    error_details: List[ErrorDetail]


# 例外処理クラス
class CustomApiErrorException(Exception):
    def __init__(
        self,
        error_type: ErrorType,
        message: str = "",
        error_details: List[ErrorDetail] = [],
    ):
        """_summary_
            例外処理クラス
        Args:
            error_type (ErrorType): error_type指定(※error_typeが存在しない場合は、ErrorTypeに追加してください)
            message (str, optional): エラーメッセージ.
        """
        self.error = _Error(
            status=error_type.get_http_status(),
            error=error_type.get_error(),
            error_type=error_type.get_error_type(),
            message=message,
            code=error_type.get_error_code(),
            error_details=error_details,
        )

    def get_error(self) -> dict[str, Any]:
        """errorの内容をレスポンスできる形で取得"""
        return self.error.model_dump()

    def set_message(self, message):
        """エラーメッセージを設定する"""
        self.error.message = message

    def create_error_detail(self, field, message):
        """error_detailを作成して、error_detailsに追加"""
        error_detail = ErrorDetail(field=field, message=message)
        self.error.error_details.append(error_detail)


# Request時に使うSerializeクラス。(継承して使う)
class RequestErrorSerializer(serializers.Serializer):
    """_summary_
        Request時に扱うSerializerクラスにエラーハンドリングを追加したクラス。
        ※data=request値でバリデーションチェックする際は、必ずerror_typeも指定する(指定がない場合は,エラーになります。)
    Args:
        data (_type_, optional): requestで受け取ったパタメータデータ
        error_type (ErrorType): error_type指定(※error_typeが存在しない場合は、ErrorTypeに追加してください)
    """

    def __init__(self, instance=None, data=..., error_type: ErrorType = None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self._error_exception = None
        # request値をdataに渡してSerializer使うときは、例外処理クラスのセットアップを強制する
        # swaggerなどでインスタンスのみ使用したいケースがあるため、
        # data=が引数で渡されてRequest処理行う際は、error_typeの強制をしている
        if data is not Ellipsis:
            if error_type is None:
                raise TypeError(
                    "CustomApiErrorExceptionがインスタンス化されていません。error_type(型:ErrorType)は必須の引数です。"
                )
            self._error_exception = CustomApiErrorException(error_type=error_type)

    def get_error(self) -> dict[str, Any]:
        """errorの内容をレスポンスできる形で取得(※is_validでチャック済みの時利用してください。※superのreturnを推奨)"""
        if self.errors is not None:
            # リクエスト時のSerializerでのバリデーションは、
            # self.errorsに辞書型でバリデーション結果が返ってくるので、
            # エラーレスポンスのerror_detailsに結果を自動で追加
            for key, value in self.errors.items():
                for message in value:
                    self.create_error_detail(field=key, message=message)
        return self._error_exception.error.model_dump()

    def set_message(self, message):
        """エラーメッセージを設定する"""
        self._error_exception.error.message = message

    def create_error_detail(self, field, message):
        """error_detailを作成して、error_detailsに追加"""
        error_detail = ErrorDetail(field=field, message=message)
        self._error_exception.error.error_details.append(error_detail)
