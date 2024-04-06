from typing import Dict, List
import openai
from utils.errors import CustomApiErrorException, ErrorType, ErrorDetail


class OpenAIErrorHandler:
    @staticmethod
    def handle_error(e) -> CustomApiErrorException:
        """_summary_:
            ExceptionからOpenAIErrorの判定を行い、適切なエラーを返す。
            OpenAIError以外の場合、自社サーバーエラーとしてエラーを返す。
        Args:
            e (Exception): Exceptionを代入してください。
        """
        if isinstance(e, openai.OpenAIError):
            openai_error = _OpenAiError()
            if isinstance(e, openai.AuthenticationError):
                # 認証エラーに関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI Authentication Error",
                    error_type=ErrorType.OPENAI_UNAUTHORIZED,
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            elif isinstance(e, openai.RateLimitError):
                # レート制限エラーに関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI Rate Limit Error",
                    error_type=ErrorType.OPENAI_TOO_MANY_REQUESTS,
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            elif isinstance(e, openai.APITimeoutError):
                # リクエスト時間が長いに関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI APITimeout Error",
                    error_type=ErrorType.OPENAI_GATEWAY_TIMEOUT,
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            elif isinstance(e, openai.APIConnectionError):
                # API接続エラーに関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI API Connection Error",
                    error_type=ErrorType.OPENAI_BAD_GATEWAY,
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            elif isinstance(e, openai.InternalServerError):
                # OpenAI社のエラーに関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI InternalServer Error",
                    error_type=ErrorType.OPENAI_INTERNAL_SERVER_ERROR,
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            elif isinstance(e, openai.BadRequestError):
                # リクエストの形式が不正に関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI BadRequest Error",
                    error_type=ErrorType.OPENAI_BAD_REQUEST,
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            elif isinstance(e, openai.APIError):
                # APIエラーに関する追加の処理
                return CustomApiErrorException(
                    message="OpenAI API Error",
                    error_type=openai_error.get_error_type_from_status_code(
                        int(e.status_code)
                    ),
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
            else:
                return CustomApiErrorException(
                    message="OpenAI 不明なエラー",
                    error_type=openai_error.get_error_type_from_status_code(
                        int(e.status_code)
                    ),
                    error_details=openai_error.get_openai_error_from_error_details(e),
                )
        else:
            return CustomApiErrorException(
                message="自社サーバーエラー。OpenAIにリクエストできません。",
                error_type=ErrorType.REQUEST_OPENAI_INTERNAL_SERVER_ERROR,
            )


class _OpenAiError:
    def get_error_type_from_status_code(self, status_code: int) -> ErrorType:
        error_types: Dict[int, ErrorType] = {
            400: ErrorType.OPENAI_BAD_REQUEST,
            401: ErrorType.OPENAI_UNAUTHORIZED,
            403: ErrorType.OPENAI_FORBIDDEN,
            429: ErrorType.OPENAI_TOO_MANY_REQUESTS,
            500: ErrorType.OPENAI_INTERNAL_SERVER_ERROR,
            502: ErrorType.OPENAI_BAD_GATEWAY,
            503: ErrorType.OPENAI_SERVICE_UNAVAILABLE,
            504: ErrorType.OPENAI_GATEWAY_TIMEOUT,
        }
        return error_types.get(status_code)

    def get_openai_error_from_error_details(
        self,
        e: openai.OpenAIError,
    ) -> List[ErrorDetail]:
        status_code = ErrorDetail(field="status_code", message=str(e.status_code))
        code = ErrorDetail(field="code", message=str(e.code))
        type = ErrorDetail(field="type", message=str(e.type))
        error_details: List[ErrorDetail] = [status_code, code, type]
        if e.body is not None and "message" in e.body:
            message = ErrorDetail(field="message", message=str(e.body["message"]))
            error_details.append(message)
        return error_details
