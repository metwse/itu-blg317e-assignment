"""Flask app creation and bootsrap."""

from src import log
from src.error import AppError, \
    error_handler, validation_error_handler, \
    not_found_error_handler, unspecified_error_handler
from src.routes import internal_routes, management_routes, portal_routes, public_routes
from src.state import State

from src.handlers import (
    ProviderHandler,
    UserHandler,
    EconomyHandler,
    PermissionHandler,
    IndicatorHandler,
    PortalHandler
)

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
    user_handler = UserHandler(state.user_service)
    economy_handler = EconomyHandler(state.economy_service)
    permission_handler = PermissionHandler(state.permission_service)
    indicator_handler = IndicatorHandler(state.indicator_service)

    # Portal handler needs multiple services
    portal_handler = PortalHandler(
        state.user_service,
        state.provider_service,
        state.permission_service,
        state.indicator_service,
        state.jwt_secret
    )

    if state.internal_access_token is not None:
        log.info("registered internal access routes")
        app.register_blueprint(internal_routes(state.internal_access_token,
                                               provider_handler,
                                               user_handler,
                                               economy_handler,
                                               permission_handler,
                                               indicator_handler))
    else:
        log.info("no internal access token provided, skipped internal routes")

    app.register_blueprint(management_routes(state.management_console_token,
                                             provider_handler,
                                             user_handler,
                                             permission_handler))

    app.register_blueprint(portal_routes(state.jwt_secret,
                                         portal_handler))

    # Public routes (no auth required)
    app.register_blueprint(public_routes(state.pool))

    return app
