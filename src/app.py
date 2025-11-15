from src.response import AppError, \
    error_handler, not_found_error_handler, unspecified_error_handler
from src.routes import country_routes

from src.service.country_service import CountryService
from src.handlers.country_handler import CountryHandler

from flask import Flask, jsonify
import time


def create_app(repo, loop):
    app = Flask(__name__)
    app.register_error_handler(AppError, error_handler)
    app.register_error_handler(404, not_found_error_handler)
    app.register_error_handler(Exception, unspecified_error_handler)

    service = CountryService(repo)
    country_handler = CountryHandler(service, loop)

    start_time = time.time()

    def status_handler():
        return jsonify({
            'message': "OK",
            'uptime': int(time.time() - start_time)
        })
    app.add_url_rule("/", view_func=status_handler)

    app.register_blueprint(country_routes(country_handler))

    return app
