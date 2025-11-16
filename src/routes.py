from src.handlers.country_handler import CountryHandler

from flask import Blueprint


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
