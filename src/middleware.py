from src.error import AppError, AppErrorType
from flask import request, g

import jwt


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


def portal_jwt_authorize(jwt_secret: str, exclude_paths: list[str] = None):
    """JWT authorization middleware for the Portal API.

    Validates the Bearer token from the Authorization header and extracts
    the user_id into Flask's request context (g.user_id).

    Also extracts X-Provider-Context header into g.provider_id if present.

    Args:
        jwt_secret: The secret key used to verify JWT signatures.
        exclude_paths: List of endpoint paths that don't require auth
                       (e.g., ['/auth/login']).
    """
    if exclude_paths is None:
        exclude_paths = []

    def authorize():
        # Skip auth for excluded paths (like /auth/login)
        for path in exclude_paths:
            if request.path.endswith(path):
                return

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AppError(AppErrorType.UNAUTHORIZED,
                           "Authorization header is required.")

        # Expecting "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AppError(AppErrorType.UNAUTHORIZED,
                           "Invalid Authorization header format. "
                           "Expected 'Bearer <token>'.")

        token = parts[1]

        try:
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            g.user_id = payload.get('user_id')

            if g.user_id is None:
                raise AppError(AppErrorType.UNAUTHORIZED,
                               "Token missing 'user_id' claim.")

        except jwt.ExpiredSignatureError:
            raise AppError(AppErrorType.UNAUTHORIZED, "Token has expired.")
        except jwt.InvalidTokenError as e:
            raise AppError(AppErrorType.UNAUTHORIZED,
                           f"Invalid token: {str(e)}")

        # Extract provider context header if present
        provider_context = request.headers.get('X-Provider-Context')
        if provider_context:
            try:
                g.provider_id = int(provider_context)
            except ValueError:
                raise AppError(AppErrorType.VALIDATION_ERROR,
                               "X-Provider-Context must be an integer.")
        else:
            g.provider_id = None

    return authorize
