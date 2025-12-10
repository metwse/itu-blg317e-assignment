from src.handlers.base_handler import BaseHandler
from src.handlers.provider_handler import ProviderHandler
from src.handlers.economy_handler import EconomyHandler
from src.handlers.permission_handler import PermissionHandler

from src.middleware import internal_access_authorize

from flask import Blueprint


def internal_routes(internal_access_token: str,
                    provider_handler,
                    economy_handler,
                    permission_handler,
                    health_indicator_handler,
                    economic_indicator_handler,
                    environment_indicator_handler):
    """Aggregates all internal sub-routes and applies authentication
    middleware.
    """

    internal = Blueprint("internal", __name__, url_prefix="/internal")

    internal.register_blueprint(provider_routes(provider_handler))
    internal.register_blueprint(economy_routes(economy_handler))
    internal.register_blueprint(permission_routes(permission_handler))
    internal.register_blueprint(
        indicator_routes("health_indicators",
                         health_indicator_handler))
    internal.register_blueprint(
        indicator_routes("economic_indicators",
                         economic_indicator_handler))
    internal.register_blueprint(
        indicator_routes("environment_indicators",
                         environment_indicator_handler))

    internal.before_request(internal_access_authorize(internal_access_token))

    return internal


def provider_routes(provider_handler: ProviderHandler):
    """Creates CRUD routes for Providers."""

    providers = Blueprint("providers", __name__, url_prefix="/providers")

    providers.add_url_rule("/",
                           view_func=provider_handler.list,
                           methods=["GET"])

    providers.add_url_rule("/",
                           view_func=provider_handler.create,
                           methods=["POST"])

    async def get(id):
        return await provider_handler.get(int(id))
    providers.add_url_rule("/<id>", view_func=get, methods=["GET"])

    async def update(id):
        return await provider_handler.update(int(id))
    providers.add_url_rule("/<id>", view_func=update, methods=["PATCH"])

    async def delete(id):
        return await provider_handler.delete(int(id))
    providers.add_url_rule("/<id>", view_func=delete, methods=["DELETE"])

    return providers


def economy_routes(economy_handler: EconomyHandler):
    """Creates CRUD routes for Economyies."""

    economies = Blueprint("economies", __name__, url_prefix="/economies")

    economies.add_url_rule("/",
                           view_func=economy_handler.list,
                           methods=["GET"])

    economies.add_url_rule("/",
                           view_func=economy_handler.create,
                           methods=["POST"])

    async def get(code):
        return await economy_handler.get(code)
    economies.add_url_rule("/<code>", view_func=get, methods=["GET"])

    async def update(code):
        return await economy_handler.update(code)
    economies.add_url_rule("/<code>", view_func=update, methods=["PATCH"])

    async def delete(code):
        return await economy_handler.delete(code)
    economies.add_url_rule("/<code>", view_func=delete, methods=["DELETE"])

    return economies


def permission_routes(permission_handler: PermissionHandler):
    """Creates CRUD routes for Permissions."""

    permissions = Blueprint("permissions", __name__, url_prefix="/permissions")

    permissions.add_url_rule("/",
                             view_func=permission_handler.list,
                             methods=["GET"])

    permissions.add_url_rule("/",
                             view_func=permission_handler.create,
                             methods=["POST"])

    async def get(provider_id, economy_code):
        return await permission_handler.get(int(provider_id), economy_code)
    permissions.add_url_rule("/<provider_id>/<economy_code>",
                             view_func=get, methods=["GET"])

    async def update(provider_id, economy_code):
        return await permission_handler.update(int(provider_id), economy_code)
    permissions.add_url_rule("/<provider_id>/<economy_code>",
                             view_func=update, methods=["PATCH"])

    async def delete(provider_id, economy_code):
        return await permission_handler.delete(int(provider_id), economy_code)
    permissions.add_url_rule("/<provider_id>/<economy_code>",
                             view_func=delete, methods=["DELETE"])

    return permissions


def indicator_routes(name: str, indicator: BaseHandler):
    """Creates CRUD routes for Indicators."""

    indicators = Blueprint(name, __name__, url_prefix=f"/{name}")

    indicators.add_url_rule("/", view_func=indicator.list, methods=["GET"])

    indicators.add_url_rule("/", view_func=indicator.create, methods=["POST"])

    async def get(provider_id, economy_code, year):
        return await indicator.get(int(provider_id), economy_code,
                                   int(year))
    indicators.add_url_rule("/<provider_id>/<economy_code>/<year>",
                            view_func=get, methods=["GET"])

    async def update(provider_id, economy_code, year):
        return await indicator.update(int(provider_id), economy_code,
                                      int(year))
    indicators.add_url_rule("/<provider_id>/<economy_code>/<year>",
                            view_func=update, methods=["PATCH"])

    async def delete(provider_id, economy_code, year):
        return await indicator.delete(int(provider_id), economy_code,
                                      int(year))

    indicators.add_url_rule("/<provider_id>/<economy_code>/<year>",
                            view_func=delete, methods=["DELETE"])

    return indicators
