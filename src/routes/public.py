"""Public API routes for viewing data (no authentication required)."""

from flask import Blueprint

from src.handlers.public_handler import PublicHandler


def public_routes(handler: PublicHandler):
    """Create public API routes for viewing indicator data with joins.

    Args:
        handler: PublicHandler instance for handling requests.

    Returns:
        Flask Blueprint with public data routes.
    """
    public = Blueprint("public", __name__, url_prefix="/api/public")

    public.add_url_rule(
        "/economies", view_func=handler.list_economies, methods=["GET"])
    public.add_url_rule(
        "/regions", view_func=handler.list_regions, methods=["GET"])
    public.add_url_rule(
        "/income-levels", view_func=handler.list_income_levels, methods=["GET"])
    public.add_url_rule(
        "/providers", view_func=handler.list_providers, methods=["GET"])
    public.add_url_rule(
        "/indicators", view_func=handler.list_indicators, methods=["GET"])
    public.add_url_rule(
        "/indicators/economic",
        view_func=handler.list_economic_indicators, methods=["GET"])
    public.add_url_rule(
        "/indicators/health",
        view_func=handler.list_health_indicators, methods=["GET"])
    public.add_url_rule(
        "/indicators/environment",
        view_func=handler.list_environment_indicators, methods=["GET"])
    public.add_url_rule(
        "/stats", view_func=handler.get_stats, methods=["GET"])

    return public
