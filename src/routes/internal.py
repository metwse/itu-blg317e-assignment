from src.handlers.provider_handler import ProviderHandler, UserHandler
from src.handlers.economy_handler import EconomyHandler
from src.handlers.permission_handler import PermissionHandler
from src.handlers.indicator_handler import IndicatorHandler

from src.middleware import internal_access_authorize

from flask import Blueprint


def internal_routes(internal_access_token: str,
                    provider_handler: ProviderHandler,
                    user_handler: UserHandler,
                    economy_handler: EconomyHandler,
                    permission_handler: PermissionHandler,
                    indicator_handler: IndicatorHandler):
    """Aggregates all internal sub-routes and applies authentication
    middleware.
    """

    internal = Blueprint("internal", __name__, url_prefix="/internal")

    internal.register_blueprint(provider_routes(provider_handler))
    internal.register_blueprint(user_routes(user_handler))
    internal.register_blueprint(economy_routes(economy_handler))
    internal.register_blueprint(permission_routes(permission_handler))

    internal.register_blueprint(indicator_routes(indicator_handler))

    internal.before_request(internal_access_authorize(internal_access_token))

    return internal


def provider_routes(provider_handler: ProviderHandler):
    """Creates CRUD routes for Providers."""
    providers = Blueprint("providers", __name__, url_prefix="/providers")

    providers.add_url_rule("/", view_func=provider_handler.list,
                           methods=["GET"])
    providers.add_url_rule("/", view_func=provider_handler.create,
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


def user_routes(user_handler: UserHandler):
    """Creates CRUD routes for Providers."""
    users = Blueprint("users", __name__, url_prefix="/users")

    users.add_url_rule("/", view_func=user_handler.list, methods=["GET"])
    users.add_url_rule("/", view_func=user_handler.create, methods=["POST"])

    async def get(id):
        return await user_handler.get(int(id))
    users.add_url_rule("/<id>", view_func=get, methods=["GET"])

    async def update(id):
        return await user_handler.update(int(id))
    users.add_url_rule("/<id>", view_func=update, methods=["PATCH"])

    async def delete(id):
        return await user_handler.delete(int(id))
    users.add_url_rule("/<id>", view_func=delete, methods=["DELETE"])

    return users


def economy_routes(economy_handler: EconomyHandler):
    """Creates CRUD routes for Economies."""
    economies = Blueprint("economies", __name__, url_prefix="/economies")

    economies.add_url_rule("/", view_func=economy_handler.list,
                           methods=["GET"])
    economies.add_url_rule("/", view_func=economy_handler.create,
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
    """Creates CRUD routes for Permissions.
    Updated to use surrogate 'id' instead of composite keys.
    """
    permissions = Blueprint("permissions", __name__, url_prefix="/permissions")

    permissions.add_url_rule("/", view_func=permission_handler.list,
                             methods=["GET"])
    permissions.add_url_rule("/", view_func=permission_handler.create,
                             methods=["POST"])

    async def get(id):
        return await permission_handler.get(int(id))
    permissions.add_url_rule("/<id>", view_func=get, methods=["GET"])

    async def update(id):
        return await permission_handler.update(int(id))
    permissions.add_url_rule("/<id>", view_func=update, methods=["PATCH"])

    async def delete(id):
        return await permission_handler.delete(int(id))
    permissions.add_url_rule("/<id>", view_func=delete, methods=["DELETE"])

    return permissions


def indicator_routes(indicator_handler: IndicatorHandler):
    """Creates CRUD routes for Unified Indicators."""
    indicators = Blueprint("indicators", __name__, url_prefix="/indicators")

    indicators.add_url_rule("/", view_func=indicator_handler.list,
                            methods=["GET"])
    indicators.add_url_rule("/", view_func=indicator_handler.create,
                            methods=["POST"])

    async def get(provider_id, economy_code, year):
        return await indicator_handler.get(int(provider_id), economy_code,
                                           int(year))
    indicators.add_url_rule("/<provider_id>/<economy_code>/<year>",
                            view_func=get, methods=["GET"])

    async def update(provider_id, economy_code, year):
        return await indicator_handler.update(int(provider_id), economy_code,
                                              int(year))
    indicators.add_url_rule("/<provider_id>/<economy_code>/<year>",
                            view_func=update, methods=["PATCH"])

    async def delete(provider_id, economy_code, year):
        return await indicator_handler.delete(int(provider_id), economy_code,
                                              int(year))
    indicators.add_url_rule("/<provider_id>/<economy_code>/<year>",
                            view_func=delete, methods=["DELETE"])

    return indicators
