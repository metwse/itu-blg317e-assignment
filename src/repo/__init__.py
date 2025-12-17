from .base_repo import BaseRepo

from src.dto import (
    EconomyUpdateDto, EconomyCreateDto,
    PermissionUpdateDto, PermissionCreateDto,
    ProviderCreateDto, ProviderUpdateDto,
    UserCreateDto, UserUpdateDto,
    IndicatorUpdateDto, IndicatorCreateDto
)
from src.entities import (
    Economy, Permission, Provider, Indicator, User
)


class ProviderRepo(BaseRepo[Provider, ProviderUpdateDto, ProviderCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'providers', ['id'],
                         (Provider, ProviderUpdateDto, ProviderCreateDto))


class UserRepo(BaseRepo[User, UserUpdateDto, UserCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'users', ['id'],
                         (User, UserUpdateDto, UserCreateDto))


class EconomyRepo(BaseRepo[Economy, EconomyUpdateDto, EconomyCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'economies', ['code'],
                         (Economy, EconomyUpdateDto, EconomyCreateDto))


class PermissionRepo(BaseRepo[Permission, PermissionUpdateDto,
                              PermissionCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'permissions', ['id'],
                         (Permission, PermissionUpdateDto,
                          PermissionCreateDto))


class IndicatorRepo(BaseRepo[Indicator, IndicatorUpdateDto,
                             IndicatorCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'indicators',
                         ['provider_id', 'economy_code', 'year'],
                         (Indicator, IndicatorUpdateDto, IndicatorCreateDto))


__all__ = ['EconomyRepo', 'ProviderRepo', 'PermissionRepo', 'IndicatorRepo']
