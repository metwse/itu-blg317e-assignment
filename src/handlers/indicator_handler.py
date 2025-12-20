from .base_handler import BaseHandler

from src.service import IndicatorService


class IndicatorHandler(BaseHandler):
    service: IndicatorService

    def __init__(self, service: IndicatorService):
        super().__init__(service)
