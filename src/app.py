from flask import Flask, jsonify
import time

from src.routes import country_routes

from .service.country_service import CountryService
from .handlers.country_handler import CountryHandler


def create_app(repo, loop):
    app = Flask(__name__)
    service = CountryService(repo)
    country_handler = CountryHandler(service, loop)

    start_time = time.time()

    def status_handler():
        return jsonify({
                "message": "OK",
                "uptime": int(time.time() - start_time)
            })

    app.register_blueprint(country_routes(country_handler))

    app.add_url_rule("/", view_func=status_handler)

    return app
