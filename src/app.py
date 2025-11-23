from src import log
from src.error import AppError, \
    error_handler, validation_error_handler, \
    not_found_error_handler, unspecified_error_handler
from src.routes import internal_routes

from src.service import ProviderService, CountryService, PermissionService
from src.handlers.provider_handler import ProviderHandler
from src.handlers.country_handler import CountryHandler
from src.handlers.permission_handler import PermissionHandler

from pydantic_core import ValidationError
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import time


def create_app(pool, internal_access_token: str | None = None):
    app = Flask(__name__, static_folder='static', static_url_path='')
    CORS(app)

    app.register_error_handler(AppError, error_handler)
    app.register_error_handler(404, not_found_error_handler)
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(Exception, unspecified_error_handler)

    provider_handler = ProviderHandler(ProviderService(pool))
    country_handler = CountryHandler(CountryService(pool))
    permission_handler = PermissionHandler(PermissionService(pool))

    start_time = time.time()

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/status')
    def status_handler():
        return jsonify({
            'message': "OK",
            'uptime': int(time.time() - start_time)
        })

    if internal_access_token is not None:
        log.info("registered internal access routes")
        app.register_blueprint(internal_routes(internal_access_token,
                                               provider_handler,
                                               country_handler,
                                               permission_handler))
    else:
        log.info("no internal access token provided, skipped internal routes")

    return app
