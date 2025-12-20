from . import BaseService

from src.repo import EconomyRepo


class EconomyService(BaseService):
    repo: EconomyRepo

    def __init__(self, pool):
        super().__init__(EconomyRepo(pool))
