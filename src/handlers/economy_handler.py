from .base_handler import BaseHandler

from src.service import EconomyService


class EconomyHandler(BaseHandler):
    def __init__(self, service: EconomyService):
        super().__init__(service)
