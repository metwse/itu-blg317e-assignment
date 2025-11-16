from src.handlers.provider_handler import ProviderHandler
from src.handlers.country_handler import CountryHandler
from src.handlers.permission_handler import PermissionHandler

from flask import Blueprint


def provider_routes(provider_handler: ProviderHandler):
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


def country_routes(country_handler: CountryHandler):
    countries = Blueprint("countries", __name__, url_prefix="/countries")

    countries.add_url_rule("/",
                           view_func=country_handler.list,
                           methods=["GET"])

    countries.add_url_rule("/",
                           view_func=country_handler.create,
                           methods=["POST"])

    async def get(code):
        return await country_handler.get(code)
    countries.add_url_rule("/<code>", view_func=get, methods=["GET"])

    async def update(code):
        return await country_handler.update(code)
    countries.add_url_rule("/<code>", view_func=update, methods=["PATCH"])

    async def delete(code):
        return await country_handler.delete(code)
    countries.add_url_rule("/<code>", view_func=delete, methods=["DELETE"])

    return countries


def permission_routes(permission_handler: PermissionHandler):
    permissions = Blueprint("permissions", __name__, url_prefix="/permissions")

    permissions.add_url_rule("/",
                             view_func=permission_handler.list,
                             methods=["GET"])

    permissions.add_url_rule("/",
                             view_func=permission_handler.create,
                             methods=["POST"])

    async def get(provider_id, country_code):
        return await permission_handler.get(int(provider_id), country_code)
    permissions.add_url_rule("/<provider_id>/<country_code>",
                             view_func=get, methods=["GET"])

    async def update(provider_id, country_code):
        return await permission_handler.update(int(provider_id), country_code)
    permissions.add_url_rule("/<provider_id>/<country_code>",
                             view_func=update, methods=["PATCH"])

    async def delete(provider_id, country_code):
        return await permission_handler.delete(int(provider_id), country_code)
    permissions.add_url_rule("/<provider_id>/<country_code>",
                             view_func=delete, methods=["DELETE"])

    return permissions
