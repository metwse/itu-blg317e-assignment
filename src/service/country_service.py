from .base_service import BaseService

from src.repo import CountryRepo


class CountryService(BaseService):
    def __init__(self, pool):
        super().__init__(CountryRepo(pool))
