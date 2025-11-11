from flask import Blueprint
from src.handlers.economic_handler import EconomicHandler

def economic_routes(handler: EconomicHandler):
    econ = Blueprint("economic", __name__, url_prefix="/economic")

    econ.add_url_rule(
        "/<code>",
        view_func=handler.list_indicators,
        methods=["GET"],
    )

    econ.add_url_rule(
        "/",
        view_func=handler.create_indicator,
        methods=["POST"],
    )

    return econ
