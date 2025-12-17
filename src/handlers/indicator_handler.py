from .base_handler import BaseHandler

from src.service import IndicatorService


class IndicatorHandler(BaseHandler):
    def __init__(self, service: IndicatorService):
        super().__init__(service)
