from . import BaseService

from src.repo import IndicatorRepo


class IndicatorService(BaseService):
    def __init__(self, pool):
        super().__init__(IndicatorRepo(pool))
