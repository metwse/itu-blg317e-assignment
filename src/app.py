from flask import Flask, request, jsonify
import time
import asyncio

from repo.mock_country_repo import MockCountryRepo
from service.country_service import CountryService


def create_app(repo=None):
    """Create Flask app. Accepts an optional repo for dependency injection.

    If no repo is provided, a `MockCountryRepo` is used so the app can run
    locally without a database.
    """
    start = time.time()

    def status():
        return {"message": "OK", "uptime": int(time.time() - start)}

    app = Flask(__name__)

    # setup repo/service
    repo = repo or MockCountryRepo()
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
        try:
            res = asyncio.run(service.create_country(code, name))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"result": res}), 201

    return app
