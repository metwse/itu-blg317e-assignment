from .base_service import BaseService

from src.repo import EconomyRepo


class EconomyService(BaseService):
    def __init__(self, pool):
        super().__init__(EconomyRepo(pool))
