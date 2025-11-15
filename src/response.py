from src import log

from enum import Enum
from typing import Any
import json

from werkzeug.wrappers.response import Response


class AppErorrType(Enum):
    NOT_FOUND = 0
    UNAUTHORIZED = 1
    DUPLICATE_ENTRY = 2
    INTERNAL_ERROR = 3

    details: Any

    def code(self) -> int:
        match self:
            case AppErorrType.NOT_FOUND:
                return 404
            case AppErorrType.UNAUTHORIZED:
                return 401
            case AppErorrType.DUPLICATE_ENTRY:
                return 400
            case AppErorrType.INTERNAL_ERROR:
                return 500


class AppError(Exception):
    details: Any
    error_type: AppErorrType

    def __init__(self, error_type: AppErorrType, details: Any = None):
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
            'details': e.details
        }),
        mimetype='application/json',
        status=e.code
    )


def unspecified_error_handler(e: Exception) -> Response:
    return error_handler(AppError(AppErorrType.INTERNAL_ERROR, details=e))


def not_found_error_handler(_) -> Response:
    return error_handler(AppError(AppErorrType.NOT_FOUND, "route not found"))
