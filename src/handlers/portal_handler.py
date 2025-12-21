"""Portal API Handler for data entry operations.

This handler manages authentication, permission viewing, and indicator
data entry for Provider Administrators and Technical Accounts.
"""

from .util import json

from src.error import AppError, AppErrorType
from src.service import (
    UserService,
    ProviderService,
    PermissionService,
    IndicatorService
)

from flask import jsonify, request, g
import jwt
from datetime import datetime, timedelta, timezone


class PortalHandler:
    """Handler for /api/portal endpoints."""

    user_service: UserService
    provider_service: ProviderService
    permission_service: PermissionService
    indicator_service: IndicatorService
    jwt_secret: str

    def __init__(self,
                 user_service: UserService,
                 provider_service: ProviderService,
                 permission_service: PermissionService,
                 indicator_service: IndicatorService,
                 jwt_secret: str):
        # Portal handler doesn't use a single service like BaseHandler
        self.user_service = user_service
        self.provider_service = provider_service
        self.permission_service = permission_service
        self.indicator_service = indicator_service
        self.jwt_secret = jwt_secret

    # -------------------------------------------------------------------------
    # Authentication Endpoints
    # -------------------------------------------------------------------------

    async def login(self):
        """POST /auth/login - Authenticate user and return JWT token."""
        payload = json()

        email = payload.get('email')
        password = payload.get('password')

        if not email or not password:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Email and password are required.")

        # Fetch user by email
        user = await self.user_service.get_user_by_email(email)

        if not user:
            raise AppError(AppErrorType.UNAUTHORIZED,
                           "Invalid email or password.")

        # Verify password (plain text comparison for now)
        if user['password'] != password:
            raise AppError(AppErrorType.UNAUTHORIZED,
                           "Invalid email or password.")

        # Generate JWT token
        token_payload = {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }

        token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')

        return jsonify({'token': token})

    async def get_me(self):
        """GET /auth/me - Get current user profile and managed providers."""
        user_id = g.user_id

        # Fetch user info
        user = await self.user_service.get_user_by_id(user_id)

        if not user:
            raise AppError(AppErrorType.NOT_FOUND, "User not found.")

        # Fetch providers where user is admin or technical account
        providers = await self.provider_service.get_providers_by_user(user_id)

        # Filter out immutable providers (they can't log in)
        managed_providers = [
            {
                'id': p['id'],
                'name': p['name'],
                'role': p['role']
            }
            for p in providers if not p.get('immutable', False)
        ]

        return jsonify({
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'managed_providers': managed_providers
        })

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    async def _validate_provider_context(self):
        """Validate that user has access to the provider in X-Provider-Context.

        Returns:
            The provider info dict if valid.

        Raises:
            AppError: If context is missing, invalid, or user lacks access.
        """
        user_id = g.user_id
        provider_id = g.provider_id

        if provider_id is None:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "X-Provider-Context header is required.")

        # Check if user has access to this provider
        access = await self.provider_service.validate_user_provider_access(
            user_id, provider_id
        )

        if not access:
            raise AppError(AppErrorType.FORBIDDEN,
                           "You do not have access to this provider.")

        if access.get('immutable', False):
            raise AppError(AppErrorType.FORBIDDEN,
                           "This provider is frozen and cannot submit data.")

        return access

    # -------------------------------------------------------------------------
    # Permission Endpoints
    # -------------------------------------------------------------------------

    async def list_my_permissions(self):
        """GET /permissions - List permissions for the current provider context."""
        await self._validate_provider_context()

        permissions = await self.permission_service.get_permissions_for_portal(
            g.provider_id
        )

        return jsonify(permissions)

    # -------------------------------------------------------------------------
    # Indicator Endpoints
    # -------------------------------------------------------------------------

    async def get_indicator(self):
        """GET /indicators - Get existing indicator data for economy/year."""
        await self._validate_provider_context()

        economy_code = request.args.get('economy_code')
        year = request.args.get('year')

        if not economy_code:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Query parameter 'economy_code' is required.")

        if not year:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Query parameter 'year' is required.")

        try:
            year = int(year)
        except ValueError:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "'year' must be an integer.")

        economy_code = economy_code.strip().upper()

        indicator = await self.indicator_service.get_indicator(
            g.provider_id, economy_code, year
        )

        if not indicator:
            raise AppError(AppErrorType.NOT_FOUND,
                           f"No indicator data found for {economy_code}/{year}.")

        return jsonify(indicator)

    async def upsert_indicator(self):
        """POST /indicators - Insert or update indicator data."""
        await self._validate_provider_context()

        payload = json()

        economy_code = payload.get('economy_code')
        year = payload.get('year')

        if not economy_code:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "'economy_code' is required.")

        if year is None:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "'year' is required.")

        try:
            year = int(year)
        except (ValueError, TypeError):
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "'year' must be an integer.")

        economy_code = economy_code.strip().upper()

        # Check if provider has permission for this economy/year
        permission = await self.permission_service.check_permission_for_economy(
            g.provider_id, economy_code, year
        )

        if not permission:
            raise AppError(AppErrorType.FORBIDDEN,
                           f"You do not have permission to enter data for "
                           f"{economy_code} in year {year}.")

        # Extract indicator fields from payload (excluding keys)
        indicator_data = {k: v for k, v in payload.items()
                          if k not in ('economy_code', 'year', 'provider_id')}

        try:
            result, was_created = await self.indicator_service.upsert_indicator(
                g.provider_id, economy_code, year, indicator_data
            )

            status_code = 201 if was_created else 200
            return jsonify(result), status_code

        except Exception as e:
            if "foreign key constraint" in str(e).lower():
                raise AppError(AppErrorType.VALIDATION_ERROR,
                               f"Invalid economy_code: '{economy_code}' "
                               "does not exist.")
            raise e
