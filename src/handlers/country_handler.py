from .base_handler import BaseHandler

from src.service import CountryService


class CountryHandler(BaseHandler):
    def __init__(self, service: CountryService):
        super().__init__(service)
