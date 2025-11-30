from .base_handler import BaseHandler

from src.service import HealthIndicatorService, EconomicIndicatorService, \
    EnvironmentIndicatorService


class HealthIndicatorHandler(BaseHandler):
    def __init__(self, service: HealthIndicatorService):
        super().__init__(service)


class EconomicIndicatorHandler(BaseHandler):
    def __init__(self, service: EconomicIndicatorService):
        super().__init__(service)


class EnvironmentIndicatorHandler(BaseHandler):
    def __init__(self, service: EnvironmentIndicatorService):
        super().__init__(service)
