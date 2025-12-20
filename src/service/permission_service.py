from . import BaseService

from src.repo import PermissionRepo


class PermissionService(BaseService):
    repo: PermissionRepo

    def __init__(self, pool):
        super().__init__(PermissionRepo(pool))
