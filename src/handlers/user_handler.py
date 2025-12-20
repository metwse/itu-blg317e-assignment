from .base_handler import BaseHandler
from .util import json

from src.error import AppError, AppErrorType
from src.service import UserService

from flask import jsonify


class UserHandler(BaseHandler):
    service: UserService

    def __init__(self, service: UserService):
        super().__init__(service)

    async def get_all_users(self):  # MANAGEMENT
        return jsonify(
            await self.service.get_all_users()
        )

    async def create_user(self):  # MANAGEMENT
        payload = json()

        email = payload.get("email")
        password = payload.get("password")
        name = payload.get("name")

        if not all([email, password, name]):
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Fields 'email', 'password', and 'name' are "
                           "required.")

        if '@' not in email:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Invalid email.")

        try:
            res = await self.service.create_user(email, password, name)
            return jsonify(res), 201
        except Exception:
            raise AppError(AppErrorType.ALREADY_EXITS,
                           f"User with email '{email}' already exists.")

    async def delete_user(self, id):  # MANAGEMENT
        try:
            res = await self.service.delete_user(int(id))
        except Exception:
            raise AppError(AppErrorType.FK_VIOLATION,
                           f"Could not delete user with id {id}. There may be "
                           "a provider referencing this user.")

        if not res:
            raise AppError(AppErrorType.NOT_FOUND, f"User with id {id} not "
                           "found.")

        return jsonify(res)

    async def reset_password(self, id):  # MANAGEMENT
        payload = json()
        new_password = payload.get("password")

        if not new_password:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Password is required.")

        if len(new_password) < 6:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "Password too short.")

        res = await self.service.reset_password(int(id), new_password)

        if not res:
            raise AppError(AppErrorType.NOT_FOUND,
                           f"User with id {id} not found.")

        return jsonify({'id': res['id']})
