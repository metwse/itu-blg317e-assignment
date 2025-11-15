from pydantic_core import ValidationError
from enum import Enum
from typing import Any

import json
import structlog
from werkzeug.wrappers.response import Response

log = structlog.get_logger(__name__)


class AppErrorType(Enum):
    NOT_FOUND = 0
    UNAUTHORIZED = 1
    JSON_PARSE_ERROR = 2
    INTERNAL_ERROR = 3
    VALIDATION_ERROR = 4
    ALREADY_EXITS = 5

    details: Any

    def code(self) -> int:
        match self:
            case AppErrorType.NOT_FOUND:
                return 404
            case AppErrorType.UNAUTHORIZED:
                return 401
            case AppErrorType.JSON_PARSE_ERROR \
                    | AppErrorType.VALIDATION_ERROR \
                    | AppErrorType.ALREADY_EXITS:
                return 400
            case AppErrorType.INTERNAL_ERROR:
                return 500


class AppError(Exception):
    details: Any
    error_type: AppErrorType

    def __init__(self, error_type: AppErrorType, details: Any = None):
        self.details = details
        self.error_type = error_type

    @property
    def name(self) -> str:
        return self.error_type.name

    @property
    def code(self) -> int:
        return self.error_type.code()


def error_handler(e: AppError) -> Response:
    if (e.name == 'INTERNAL_ERROR'):
        log.error("blocked a sent of internal error", details=e.details)
        e.details = "details redacted to not leak sensitive information"

    return Response(
        json.dumps({
            'error': e.name,
            'details': e.details,
            'code': e.code,
        }),
        mimetype='application/json',
        status=e.code
    )


def unspecified_error_handler(e: Exception) -> Response:
    return error_handler(AppError(AppErrorType.INTERNAL_ERROR, e))


def not_found_error_handler(_) -> Response:
    return error_handler(AppError(AppErrorType.NOT_FOUND, "route not found"))


def validation_error_handler(e: ValidationError) -> Response:
    return error_handler(AppError(AppErrorType.VALIDATION_ERROR,
                                  details=str(e)))
