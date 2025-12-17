from .base_handler import BaseHandler

from src.service import ProviderService, UserService


class ProviderHandler(BaseHandler):
    def __init__(self, service: ProviderService):
        super().__init__(service)


class UserHandler(BaseHandler):
    def __init__(self, service: UserService):
        super().__init__(service)
