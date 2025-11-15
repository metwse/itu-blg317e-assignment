from src import AppError, AppErrorType
from src.entities import Country

from flask import request, jsonify


class CountryHandler:
    def __init__(self, service):
        self.service = service

    async def list_countries(self):
        try:
            limit = int(request.args.get("limit", 100))
            offset = int(request.args.get("offset", 0))
        except ValueError:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "limit and offset must be integers")

        countries = await self.service.list_countries(limit=limit,
                                                      offset=offset)

        return jsonify(countries)

    async def get_country(self, code: str):
        result = await self.service.get_country(code)

        if result:
            return jsonify(result)
        else:
            raise AppError(AppErrorType.NOT_FOUND, "country not found")

    async def create_country(self):
        data = request.get_json()

        if not data:
            return jsonify(
                {"error": "Invalid or empty JSON body"}
            ), 400

        country = Country(**data)

        res = await self.service.create_country(country)

        return jsonify({"result": res}), 201
