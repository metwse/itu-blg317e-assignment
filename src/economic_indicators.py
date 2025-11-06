from flask import Flask
import time

from .service.country_service import CountryService
from .handlers.country_handler import CountryHandler
from .handlers.status_handler import StatusHandler
from .routes.country_routes import register_routes


def create_app(repo, loop):
    app = Flask(__name__)
    service = CountryService(repo)
    country_handler = CountryHandler(service, loop)
    status_handler = StatusHandler(time.time())

    register_routes(app, country_handler, status_handler)

    return app
