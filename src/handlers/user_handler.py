from .base_handler import BaseHandler

from src.service import UserService


class UserHandler(BaseHandler):
    def __init__(self, service: UserService):
        super().__init__(service)
