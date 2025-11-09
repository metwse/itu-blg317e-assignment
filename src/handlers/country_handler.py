from flask import request, jsonify
from src.entities import Country


class CountryHandler:
    def __init__(self, service, loop):
        self.service = service
        self.loop = loop

    def list_countries(self):
        try:
            limit = int(request.args.get("limit", 100))
            offset = int(request.args.get("offset", 0))
        except ValueError:
            return jsonify(
                {"error": "limit and offset must be integers"}
            ), 400

        countries = self.loop.run_until_complete(
            self.service.list_countries(limit=limit, offset=offset)
        )
        return jsonify(countries)

    def get_country(self, code: str):
        result = self.loop.run_until_complete(self.service.get_country(code))

        if result:
            return jsonify(result)
        else:
            return jsonify(
                {"error": f"Country with code '{code}' not found"}
            ), 404

    def create_country(self):
        data = request.get_json()

        if not data:
            return jsonify(
                {"error": "Invalid or empty JSON body"}
            ), 400

        try:
            country = Country(**data)

            res = self.loop.run_until_complete(
                self.service.create_country(country)
            )

            return jsonify({"result": res}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
