from flask import Flask, request, jsonify
import time

from .service.country_service import CountryService


def create_app(repo, loop):
    start = time.time()

    def status():
        return {"message": "OK", "uptime": int(time.time() - start)}

    app = Flask(__name__)
    service = CountryService(repo)

    @app.route("/")
    def _status():
        return jsonify(status())

    @app.route("/countries", methods=("GET",))
    def list_countries():
        countries = loop.run_until_complete(service.list_countries(limit=100))
        return jsonify(countries)

    @app.route("/countries/<code>", methods=("GET",))
    def get_country(code: str):
        result = loop.run_until_complete(service.get_country(code))
        if result is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(result)

    @app.route("/countries", methods=("POST",))
    def create_country():
        payload = request.get_json(force=True)
        code = payload.get("code")
        name = payload.get("name")
        continent = payload.get("continent")
        lat = payload.get("lat")
        lng = payload.get("lng")
        try:
            res = loop.run_until_complete(service.create_country(code, name, continent, lat, lng))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"result": res}), 201

    return app
