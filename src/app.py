from flask import Flask, request, jsonify
import time
import asyncio

from .service.country_service import CountryService


def create_app(repo):
    """Create Flask app. Requires a repo for dependency injection."""
    start = time.time()

    def status():
        return {"message": "OK", "uptime": int(time.time() - start)}

    app = Flask(__name__)

    # setup service with provided repo
    service = CountryService(repo)

    @app.route("/")
    def _status():
        return jsonify(status())

    @app.route("/countries", methods=("GET",))
    def list_countries():
        # call async service from sync view
        countries = asyncio.run(service.list_countries(limit=100))
        return jsonify(countries)

    @app.route("/countries/<code>", methods=("GET",))
    def get_country(code: str):
        result = asyncio.run(service.get_country(code))
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
            res = asyncio.run(service.create_country(code, name, continent, lat, lng))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"result": res}), 201

    return app
