from .base_repo import BaseRepo

from src.dto import CountryUpdateDto, PermissionUpdateDto, \
    ProviderCreateDto, ProviderUpdateDto, EconomicIndicatorUpdateDto, \
    HealthIndicatorUpdateDto, EnvironmentIndicatorUpdateDto
from src.entities import Country, Permission, Provider, \
    EconomicIndicator, HealthIndicator, EnvironmentIndicator


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


class HealthIndicatorRepo(BaseRepo[HealthIndicator,
                          HealthIndicatorUpdateDto,
                          HealthIndicator]):
    def __init__(self, pool):
        super().__init__(pool, 'health_indicators',
                         ['provider_id', 'country_code', 'year'],
                         (HealthIndicator,
                          HealthIndicatorUpdateDto,
                          HealthIndicator))


class EconomicIndicatorRepo(BaseRepo[EconomicIndicator,
                            EconomicIndicatorUpdateDto,
                            EconomicIndicator]):
    def __init__(self, pool):
        super().__init__(pool, 'economic_indicators',
                         ['provider_id', 'country_code', 'year'],
                         (EconomicIndicator,
                          EconomicIndicatorUpdateDto,
                          EconomicIndicator))


class EnvironmentIndicatorRepo(BaseRepo[EnvironmentIndicator,
                               EnvironmentIndicatorUpdateDto,
                               EnvironmentIndicator]):
    def __init__(self, pool):
        super().__init__(pool, 'environment_indicators',
                         ['provider_id', 'country_code', 'year'],
                         (EnvironmentIndicator,
                          EnvironmentIndicatorUpdateDto,
                          EnvironmentIndicator))


__all__ = ['CountryRepo', 'ProviderRepo', 'PermissionRepo',
           'EconomicIndicatorRepo', 'HealthIndicatorRepo',
           'EnvironmentIndicatorRepo']
