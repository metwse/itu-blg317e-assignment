from src.error import AppError, \
    error_handler, validation_error_handler, \
    not_found_error_handler, unspecified_error_handler
from src.routes import provider_routes, country_routes, permission_routes

from src.service import ProviderService, CountryService, PermissionService
from src.handlers.provider_handler import ProviderHandler
from src.handlers.country_handler import CountryHandler
from src.handlers.permission_handler import PermissionHandler

from pydantic_core import ValidationError
from flask import Flask, jsonify
import time


def create_app(pool):
    app = Flask(__name__)

    app.register_error_handler(AppError, error_handler)
    app.register_error_handler(404, not_found_error_handler)
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(Exception, unspecified_error_handler)

    provider_handler = ProviderHandler(ProviderService(pool))
    country_handler = CountryHandler(CountryService(pool))
    permission_handler = PermissionHandler(PermissionService(pool))

    start_time = time.time()

    def status_handler():
        return jsonify({
            'message': "OK",
            'uptime': int(time.time() - start_time)
        })
    app.add_url_rule("/", view_func=status_handler)

    app.register_blueprint(provider_routes(provider_handler))
    app.register_blueprint(country_routes(country_handler))
    app.register_blueprint(permission_routes(permission_handler))

    return app
