from .base_handler import BaseHandler
from .util import json

from src.dto import PermissionCreateDto
from src.service import PermissionService
from src.error import AppError, AppErrorType

from flask import jsonify, request


class PermissionHandler(BaseHandler):
    service: PermissionService

    def __init__(self, service: PermissionService):
        super().__init__(service)

    async def list_permissions(self):  # MANAGEMENT
        try:
            provider_id = request.args.get("provider_id")
            if not provider_id:
                raise ValueError
            pid = int(provider_id)
        except ValueError:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Query parameter 'provider_id' is required and "
                           "must be an integer.")

        perms = await self.service.get_permissions_by_provider(pid)
        return jsonify(perms)

    async def create_permission(self):  # MANAGEMENT
        payload = PermissionCreateDto(**json())

        if payload.year_end < payload.year_start:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Range start cannot be larger than end.")

        try:
            res = await self.service.create_permission(
                payload.provider_id,
                payload.year_start,
                payload.year_end,
                payload.economy_code,
                payload.region,
                payload.footnote
            )
            return jsonify(res), 201

        except Exception as e:
            if "foreign key constraint" in str(e).lower():
                raise AppError(AppErrorType.VALIDATION_ERROR,
                               "Invalid provider_id, economy_code, or "
                               "region code.")

            if "unique constraint" in str(e).lower():
                raise AppError(AppErrorType.ALREADY_EXITS,
                               "This permission scope already exists for "
                               "the provider.")
            raise e

    async def delete_permission(self, id: int):  # MANAGEMENT
        res = await self.service.delete_permission(int(id))

        if not res:
            raise AppError(AppErrorType.NOT_FOUND,
                           f"Permission with id {id} not found.")

        return jsonify(res)
