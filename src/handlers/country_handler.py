from flask import request, jsonify


class CountryHandler:
    def __init__(self, service, loop):
        self.service = service
        self.loop = loop

    def list_countries(self):
        countries = self.loop.run_until_complete(self.service.list_countries(limit=100))
        return jsonify(countries)

    def get_country(self, code: str):
        result = self.loop.run_until_complete(self.service.get_country(code))
        return jsonify(result) if result else (jsonify({"error": "not found"}), 404)

    def create_country(self):
        data = request.get_json(force=True)
        try:
            res = self.loop.run_until_complete(
                self.service.create_country(data.get("code"), data.get("name"),
                                            data.get("continent"), data.get("lat"), data.get("lng"))
            )
            return jsonify({"result": res}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
