from .base_handler import BaseHandler

from src.service import ProviderService


class ProviderHandler(BaseHandler):
    def __init__(self, service: ProviderService):
        super().__init__(service)
