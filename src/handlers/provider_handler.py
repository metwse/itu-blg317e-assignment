from .base_handler import BaseHandler
from .util import json

from src.service import ProviderService
from src.dto import ProviderCreateDto
from src.error import AppError, AppErrorType

from flask import jsonify


class ProviderHandler(BaseHandler):
    service: ProviderService

    def __init__(self, service: ProviderService):
        super().__init__(service)

    async def get_all_providers(self):  # MANAGEMENT
        providers = await self.service.get_all_providers()
        return jsonify(providers)

    async def create_provider(self):  # MANAGEMENT
        payload = ProviderCreateDto(**json())

        try:
            res = await self.service.create_provider(
                payload.administrative_account,
                payload.technical_account,
                payload.name,
                payload.description,
                payload.website_url,
                payload.immutable
            )

            return jsonify(res), 201

        except Exception as e:
            if "foreign key constraint" in str(e).lower():
                raise AppError(AppErrorType.VALIDATION_ERROR,
                               "Provided administrative or technical account "
                               "ID does not exist.")

            if "unique constraint" in str(e).lower():
                raise AppError(AppErrorType.ALREADY_EXITS,
                               f"Provider with name '{payload.name}' already "
                               "exists.")
            raise e

    async def delete_provider(self, id: int):  # MANAGEMENT
        res = await self.service.delete_provider(int(id))

        if not res:
            raise AppError(AppErrorType.NOT_FOUND,
                           f"Provider with id {id} not found.")

        return jsonify(res)

    async def update_provider(self, id):  # MANAGEMENT
        return await self.update(int(id))
