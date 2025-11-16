from src import AppError, AppErrorType
from src.dto import CountryUpdateDto
from src.entities import Country
from src.handlers import json
from src.service.country_service import CountryService

from flask import request, jsonify


class CountryHandler:
    def __init__(self, service):
        self.service: CountryService = service

    async def list_countries(self):
        try:
            limit = int(request.args.get("limit", 100))
            offset = int(request.args.get("offset", 0))
        except ValueError:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "limit and offset must be integers")

        countries = await self.service.list_countries(limit, offset)

        return jsonify(countries)

    async def get_country(self, code: str):
        res = await self.service.get_country(code)

        if res is not None:
            return jsonify(res)
        else:
            raise AppError(AppErrorType.NOT_FOUND, "country not found")

    async def create_country(self):
        data = json()

        country = Country(**data)

        try:
            res = await self.service.create_country(country)
        except Exception:
            raise AppError(AppErrorType.ALREADY_EXITS,
                           f"country with code {data["code"]} has already "
                           "exists or the code is invalid")

        return jsonify(res), 201

    async def update_country(self, code: str):
        data = json()

        update_dto = CountryUpdateDto(**data)

        res = await self.service.update_country(code, update_dto)

        if res is not None:
            return jsonify(res)
        else:
            raise AppError(AppErrorType.VALIDATION_ERROR, "no field to update")

    async def delete_country(self, code: str):
        return jsonify(await self.service.delete_country(code))
