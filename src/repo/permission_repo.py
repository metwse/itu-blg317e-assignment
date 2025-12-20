from . import BaseRepo

from src.dto import PermissionCreateDto, PermissionUpdateDto
from src.entities import Permission


class PermissionRepo(BaseRepo[Permission, PermissionUpdateDto,
                     PermissionCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'permissions', ['id'],
                         (Permission, PermissionUpdateDto,
                          PermissionCreateDto))
