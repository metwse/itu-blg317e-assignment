from .base_service import BaseService

from src.repo import ProviderRepo, UserRepo


class ProviderService(BaseService):
    def __init__(self, pool):
        super().__init__(ProviderRepo(pool))


class UserService(BaseService):
    def __init__(self, pool):
        super().__init__(UserRepo(pool))
