"""Portal API routes for data entry operations."""

from src.handlers import PortalHandler
from src.middleware import portal_jwt_authorize

from flask import Blueprint


def portal_routes(jwt_secret: str,
                  portal_handler: PortalHandler):
    """Create and configure the Portal API blueprint.

    Args:
        jwt_secret: Secret key for JWT validation.
        portal_handler: Handler instance for portal operations.

    Returns:
        Flask Blueprint configured with portal routes.
    """
    portal = Blueprint("portal", __name__, url_prefix="/api/portal")

    # Authentication routes
    portal.add_url_rule("/auth/login",
                        view_func=portal_handler.login,
                        methods=["POST"])

    portal.add_url_rule("/auth/me",
                        view_func=portal_handler.get_me,
                        methods=["GET"])

    # Permissions routes (read-only for portal users)
    portal.add_url_rule("/permissions",
                        view_func=portal_handler.list_my_permissions,
                        methods=["GET"])

    # Indicators routes (data entry)
    portal.add_url_rule("/indicators",
                        view_func=portal_handler.get_indicator,
                        methods=["GET"])

    portal.add_url_rule("/indicators",
                        view_func=portal_handler.upsert_indicator,
                        methods=["POST"])

    # Apply JWT authorization middleware
    # Exclude /auth/login from JWT validation
    portal.before_request(
        portal_jwt_authorize(jwt_secret, exclude_paths=['/auth/login'])
    )

    return portal
