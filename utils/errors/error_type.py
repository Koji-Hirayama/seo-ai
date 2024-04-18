from enum import Enum


# HttpStatusCodeの定義
class _ErrorStatus(Enum):
    BAD_REQUEST = (400, "Bad Request")  # リクエストが不正または形式が正しくない場合
    UNAUTHORIZED = (401, "Unauthorized")  # 認証が必要なリソースに対する認証失敗
    FORBIDDEN = (403, "Forbidden")  # リソースへのアクセス権がない場合
    NOT_FOUND = (404, "Not Found")  # リクエストされたリソースが見つからない場合
    TOO_MANY_REQUESTS = (
        429,
        "Too Many Requests",
    )  # サーバー側が設定したレート制限をクライアントが超えた場合
    INTERNAL_SERVER_ERROR = (
        500,
        "Internal Server Error",
    )  # サーバー側の問題によるエラー
    BAD_GATEWAY = (
        502,
        "Bad Gateway",
    )  # APIとの間のネットワーク接続に問題がある場合
    SERVICE_UNAVAILABLE = (
        503,
        "Service Unavailable",
    )  # 過負荷またはメンテナンスのためにダウンの場合
    GATEWAY_TIMEOUT = (
        504,
        "Gateway Timeout",
    )  # 上流サーバーからのタイムリーな応答が得られなかった場合

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
    # 400 BAD_REQUEST系はE1000番台
    # =============================
    PROJECT_ID_BAD_REQUEST = ("E1001", _ErrorStatus.BAD_REQUEST)
    CREATE_TASK_BAD_REQUEST = ("E1002", _ErrorStatus.BAD_REQUEST)
    CREATE_PROJECT_BAD_REQUEST = ("E1003", _ErrorStatus.BAD_REQUEST)
    PROJECT_ID_AND_TASK_ID_BAD_REQUEST = ("E1004", _ErrorStatus.BAD_REQUEST)
    TASK_ID_BAD_REQUEST = ("E1005", _ErrorStatus.BAD_REQUEST)
    PROMPT_BAD_REQUEST = ("E1006", _ErrorStatus.BAD_REQUEST)
    SCRAPING_URL_BAD_REQUEST = ("E1007", _ErrorStatus.BAD_REQUEST)
    SCRAPING_PROMPT_MESSAGE_BAD_REQUEST = ("E1008", _ErrorStatus.BAD_REQUEST)
    # 対象がAIに関する場合は、E1100番台にする。
    # ===================================
    # AIの回答をJSONで受け取り、MODELに変更する際のバリデーションエラータイプ
    AI_MODEL_VALIDATE_JSON_BAD_REQUEST = ("E1101", _ErrorStatus.BAD_REQUEST)
    # アプリケーションで推奨するプロンプトのトークン数が上限を超える
    AI_MODEL_RECOMMENDED_PROMPT_TOKEN_LIMIT_BAD_REQUEST = (
        "E1102",
        _ErrorStatus.BAD_REQUEST,
    )
    # ===================================
    # 対象がModelの操作(CRUD)に必要なリソースを必要とした処理を意味してる場合は、E1100番台にする
    CREATE_PROMPT_BAD_REQUEST = ("E1101", _ErrorStatus.BAD_REQUEST)
    CREATE_PROMPT_OUTPUT_BAD_REQUEST = ("E1102", _ErrorStatus.BAD_REQUEST)

    # =============================
    # 404 NOT_FOUND系はE2000番台。
    # =============================
    # 対象が特定のModelを具体的に示してる場合は、E2100番台にする
    PROJECT_NOT_FOUND = ("E2101", _ErrorStatus.NOT_FOUND)
    AI_TYPE_NOT_FOUND = ("E2102", _ErrorStatus.NOT_FOUND)
    TASK_NOT_FOUND = ("E2103", _ErrorStatus.NOT_FOUND)
    AI_MODEL_NOT_FOUND = ("E2104", _ErrorStatus.NOT_FOUND)
    # ===================================
    # 対象がModelの操作(CRUD)に必要なリソースを必要とした処理を意味してる場合は、E2200番台にする
    CREATE_TASK_ELEMENT_NOT_FOUND = ("E2201", _ErrorStatus.NOT_FOUND)
    CREATE_WORK_ELEMENT_NOT_FOUND = ("E2202", _ErrorStatus.NOT_FOUND)
    CREATE_PROMPT_ELEMENT_NOT_FOUND = ("E2203", _ErrorStatus.NOT_FOUND)
    CREATE_PROMPT_OUTPUT_ELEMENT_NOT_FOUND = ("E2204", _ErrorStatus.NOT_FOUND)

    # =============================
    # 403 FORBIDDEN系はE3000番台。
    # =============================
    PROJECT_USER_FORBIDDEN = ("E3001", _ErrorStatus.FORBIDDEN)

    # =============================
    # 500 INTERNAL_SERVER_ERROR系はE4000番台。
    # =============================
    REQUEST_OPENAI_INTERNAL_SERVER_ERROR = ("E4001", _ErrorStatus.INTERNAL_SERVER_ERROR)
    CREATE_PROMPT_INTERNAL_SERVER_ERROR = ("E4002", _ErrorStatus.INTERNAL_SERVER_ERROR)
    CREATE_PROMPT_OUTPUT_INTERNAL_SERVER_ERROR = (
        "E4003",
        _ErrorStatus.INTERNAL_SERVER_ERROR,
    )

    # =============================
    # 外部APIへのリクエストエラー系は5000番台。
    # =============================
    # OpenAI系は、E5100番台にする
    OPENAI_UNAUTHORIZED = ("E5101", _ErrorStatus.UNAUTHORIZED)
    OPENAI_TOO_MANY_REQUESTS = ("E5102", _ErrorStatus.TOO_MANY_REQUESTS)
    OPENAI_GATEWAY_TIMEOUT = ("E5103", _ErrorStatus.GATEWAY_TIMEOUT)
    OPENAI_BAD_GATEWAY = ("E5104", _ErrorStatus.BAD_GATEWAY)
    OPENAI_INTERNAL_SERVER_ERROR = ("E5105", _ErrorStatus.INTERNAL_SERVER_ERROR)
    OPENAI_BAD_REQUEST = ("E5106", _ErrorStatus.BAD_REQUEST)
    OPENAI_FORBIDDEN = ("E5107", _ErrorStatus.FORBIDDEN)
    OPENAI_SERVICE_UNAVAILABLE = ("E5108", _ErrorStatus.SERVICE_UNAVAILABLE)

    # TODO: 以下、適宜エラーの識別子を定義していく。
