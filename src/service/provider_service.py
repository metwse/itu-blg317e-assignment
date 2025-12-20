from . import BaseService

from src.repo import ProviderRepo


class ProviderService(BaseService):
    def __init__(self, pool):
        super().__init__(ProviderRepo(pool))
