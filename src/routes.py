from src.handlers.country_handler import CountryHandler

from flask import Blueprint


def country_routes(country_handler: CountryHandler):
    countries = Blueprint("countries", __name__, url_prefix="/countries")

    countries.add_url_rule("/",
                           view_func=country_handler.list_countries,
                           methods=["GET"])

    countries.add_url_rule("/",
                           view_func=country_handler.create_country,
                           methods=["POST"])

    countries.add_url_rule("/<code>",
                           view_func=country_handler.get_country,
                           methods=["GET"])

    countries.add_url_rule("/<code>",
                           view_func=country_handler.update_country,
                           methods=["PATCH"])

    countries.add_url_rule("/<code>",
                           view_func=country_handler.delete_country,
                           methods=["DELETE"])

    return countries
