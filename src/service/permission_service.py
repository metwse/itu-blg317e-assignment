from . import BaseService

from src.repo import PermissionRepo


class PermissionService(BaseService):
    def __init__(self, pool):
        super().__init__(PermissionRepo(pool))
