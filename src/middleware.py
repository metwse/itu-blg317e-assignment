from src.error import AppError, AppErrorType
from flask import request


def internal_access_authorize(internal_access_token: str):
    def authorize():
        if request.headers.get('x-super-admin-secret') != \
           internal_access_token:
            raise AppError(AppErrorType.UNAUTHORIZED)

    return authorize


def management_console_authorize(management_secret: str):
    def authorize():
        if request.headers.get('x-management-secret') != \
           management_secret:
            raise AppError(AppErrorType.UNAUTHORIZED)

    return authorize
