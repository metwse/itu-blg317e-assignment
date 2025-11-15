from src.error import AppError, AppErrorType

from flask import request


def json():
    json = request.get_json()

    if not json:
        raise AppError(AppErrorType.JSON_PARSE_ERROR,
                       "could not serialize json")

    return json
