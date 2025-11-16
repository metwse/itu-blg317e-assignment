from .base_repo import BaseRepo

from src.dto import CountryUpdateDto, PermissionUpdateDto, \
    ProviderCreateDto, ProviderUpdateDto
from src.entities import Country, Permission, Provider


class ProviderRepo(BaseRepo[Provider, ProviderUpdateDto, ProviderCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'providers', ['id'],
                         (Provider, ProviderUpdateDto, ProviderCreateDto))


class CountryRepo(BaseRepo[Country, CountryUpdateDto, Country]):
    def __init__(self, pool):
        super().__init__(pool, 'countries', ['code'],
                         (Country, CountryUpdateDto, Country))


class PermissionRepo(BaseRepo[Permission, PermissionUpdateDto, Permission]):
    def __init__(self, pool):
        super().__init__(pool, 'permissions', ['provider_id', 'country_code'],
                         (Permission, PermissionUpdateDto, Permission))


__all__ = ['CountryRepo', 'ProviderRepo', 'PermissionRepo']
