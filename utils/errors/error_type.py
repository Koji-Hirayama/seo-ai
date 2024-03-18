from enum import Enum


# HttpStatusCodeの定義
class _ErrorStatus(Enum):
    BAD_REQUEST = (400, "Bad Request")  # リクエストが不正または形式が正しくない場合
    UNAUTHORIZED = (401, "Unauthorized")  # 認証が必要なリソースに対する認証失敗
    FORBIDDEN = (403, "Forbidden")  # リソースへのアクセス権がない場合
    NOT_FOUND = (404, "Not Found")  # リクエストされたリソースが見つからない場合
    INTERNAL_SERVER_ERROR = (
        500,
        "Internal Server Error",
    )  # サーバー側の問題によるエラー

    def __init__(self, http_status, error):
        self.http_status = http_status
        self.error = error


# エラーケース定義の親
class _BaseErrorTypeEnum(Enum):
    def __init__(self, error_code, error_status):
        self._error_code = error_code
        self._http_status = error_status.http_status
        self._error = error_status.error
        self._error_type = self.name

    def get_error_code(self) -> str:
        return self._error_code

    def get_http_status(self) -> int:
        return self._http_status

    def get_error(self) -> str:
        return self._error

    def get_error_type(self) -> str:
        return self._error_type


# プロジェクト内全てのエラーケースをタイプとして、定義する
# =================================================
# * 実装に応じて適宜エラータイプを追加してください
# =================================================
class ErrorType(_BaseErrorTypeEnum):
    """目的毎のエラータイプ"""

    # =============================
    # BAD_REQUEST系はE1000番台
    # =============================
    PROJECT_ID_BAD_REQUEST = ("E1001", _ErrorStatus.BAD_REQUEST)
    CREATE_TASK_BAD_REQUEST = ("E1002", _ErrorStatus.BAD_REQUEST)
    CREATE_PROJECT_BAD_REQUEST = ("E1003", _ErrorStatus.BAD_REQUEST)

    # =============================
    # NOT_FOUND系はE2000番台。
    # =============================
    # 対象が特定のModelを具体的に示してる場合は、E2100番台にする
    PROJECT_NOT_FOUND = ("E2101", _ErrorStatus.NOT_FOUND)
    AI_TYPE_NOT_FOUND = ("E2102", _ErrorStatus.NOT_FOUND)
    # 対象がModelの操作(CRUD)に必要なリソースを必要とした処理を意味してる場合は、E2100番台にする
    CREATE_TASK_NOT_FOUND = ("E2201", _ErrorStatus.NOT_FOUND)

    # TODO: 以下、適宜エラーの識別子を定義していく。
