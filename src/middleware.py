from src.error import AppError, AppErrorType
from flask import request


def internal_access_authorize(internal_access_token: str):
    def authorize():
        print(internal_access_token, request.headers.get('x-super-admin-secret'))
        if request.headers.get('x-super-admin-secret') != \
           internal_access_token:
            raise AppError(AppErrorType.UNAUTHORIZED)

    return authorize
