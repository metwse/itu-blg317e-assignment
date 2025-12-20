from . import BaseService

from src.repo import UserRepo


class UserService(BaseService):
    repo: UserRepo

    def __init__(self, pool):
        super().__init__(UserRepo(pool))
