from src.handlers import (
    ProviderHandler,
    UserHandler,
    PermissionHandler
)

from src.middleware import management_console_authorize

from flask import Blueprint


def management_routes(management_console_token,
                      provider_handler: ProviderHandler,
                      user_handler: UserHandler,
                      permission_handler: PermissionHandler):
    management = Blueprint("management", __name__, url_prefix="/management")

    management.add_url_rule("/users",
                            view_func=user_handler.get_all_users,
                            methods=["GET"])

    management.add_url_rule("/users",
                            view_func=user_handler.create_user,
                            methods=["POST"])

    management.add_url_rule("/users/<id>",
                            view_func=user_handler.delete_user,
                            methods=["DELETE"])

    management.add_url_rule("/users/<id>/reset-password",
                            view_func=user_handler.reset_password,
                            methods=["PATCH"])

    management.before_request(
        management_console_authorize(management_console_token))

    return management
