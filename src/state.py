from dataclasses import dataclass

from src.service import ProviderService, EconomyService, PermissionService
from src.service.indicator_services import EconomicIndicatorService, \
    EnvironmentIndicatorService, HealthIndicatorService


@dataclass
class State:
    provider_service: ProviderService
    economy_service: EconomyService
    permission_service: PermissionService
    health_indicator_service: HealthIndicatorService
    economic_indicator_service: EconomicIndicatorService
    environment_indicator_service: EnvironmentIndicatorService
    internal_access_token: str | None


def bootstrap_state(pool, internal_access_token: str | None = None) -> State:
    data = {}

    for key, ServiceClass in State.__annotations__.items():
        if (key.endswith('service')):
            data[key] = ServiceClass(pool)

    data['internal_access_token'] = internal_access_token

    return State(**data)
