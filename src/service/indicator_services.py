from .base_service import BaseService

from src.repo import HealthIndicatorRepo, EnvironmentIndicatorRepo, \
    EconomicIndicatorRepo


class HealthIndicatorService(BaseService):
    def __init__(self, pool):
        super().__init__(HealthIndicatorRepo(pool))


class EconomicIndicatorService(BaseService):
    def __init__(self, pool):
        super().__init__(EconomicIndicatorRepo(pool))


class EnvironmentIndicatorService(BaseService):
    def __init__(self, pool):
        super().__init__(EnvironmentIndicatorRepo(pool))
