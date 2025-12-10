from src import log
from src.error import AppError, \
    error_handler, validation_error_handler, \
    not_found_error_handler, unspecified_error_handler
from src.routes import internal_routes
from src.state import State


from src.handlers.provider_handler import ProviderHandler
from src.handlers.economy_handler import EconomyHandler
from src.handlers.permission_handler import PermissionHandler
from src.handlers.indicator_handlers import EconomicIndicatorHandler, \
    EnvironmentIndicatorHandler, HealthIndicatorHandler

from pydantic_core import ValidationError
from flask import Flask, jsonify, send_from_directory
import time


def create_app(state: State):
    static_folder: str = "static"
    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    app.register_error_handler(AppError, error_handler)
    app.register_error_handler(404, not_found_error_handler)
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(Exception, unspecified_error_handler)

    start_time = time.time()

    def index():
        return send_from_directory(static_folder, "index.html")
    app.add_url_rule("/", view_func=index)

    def status_handler():
        return jsonify({
            'message': "OK",
            'uptime': int(time.time() - start_time)
        })
    app.add_url_rule("/status", view_func=status_handler)

    provider_handler = ProviderHandler(state.provider_service)
    economy_handler = EconomyHandler(state.economy_service)
    permission_handler = PermissionHandler(state.permission_service)
    health_indicator_handler = \
        HealthIndicatorHandler(state.health_indicator_service)
    economic_indicator_handler = \
        EconomicIndicatorHandler(state.economic_indicator_service)
    environment_indicator_handler = \
        EnvironmentIndicatorHandler(state.environment_indicator_service)

    if state.internal_access_token is not None:
        log.info("registered internal access routes")
        app.register_blueprint(internal_routes(state.internal_access_token,
                                               provider_handler,
                                               economy_handler,
                                               permission_handler,
                                               health_indicator_handler,
                                               economic_indicator_handler,
                                               environment_indicator_handler))
    else:
        log.info("no internal access token provided, skipped internal routes")

    return app
