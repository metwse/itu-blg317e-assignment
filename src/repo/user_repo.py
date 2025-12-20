from . import BaseRepo

from src.dto import UserCreateDto, UserUpdateDto
from src.entities import User


class UserRepo(BaseRepo[User, UserUpdateDto, UserCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'users', ['id'],
                         (User, UserUpdateDto, UserCreateDto))
