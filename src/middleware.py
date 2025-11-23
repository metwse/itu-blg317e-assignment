from src.error import AppError, AppErrorType
from flask import request


def internal_access_authorize(internal_access_token: str):
    def authorize():
        if request.headers.get('token') != internal_access_token:
            raise AppError(AppErrorType.UNAUTHORIZED)

    return authorize
