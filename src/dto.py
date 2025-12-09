from src.entities import Region

from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProviderUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    email: Optional[str] = None
    name: Optional[str] = None
    password_hash: Optional[str] = None
    nologin: Optional[bool] = None
    is_admin: Optional[bool] = None


class ProviderCreateDto(BaseModel):
    email: str
    name: str
    password_hash: str
    nologin: bool
    is_admin: bool


class EconomyUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: Optional[str] = None
    region: Optional[Region] = None


class PermissionUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    year_start: Optional[int] = None
    year_end: Optional[int] = None


class EconomicIndicatorUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    industry: Optional[float] = None
    gdp_per_capita: Optional[float] = None
    trade: Optional[float] = None
    agriculture_forestry_and_fishing: Optional[float] = None


class HealthIndicatorUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    community_health_workers: Optional[int] = None
    prevalence_of_undernourishment: Optional[float] = None
    prevalence_of_severe_food_insecurity: Optional[float] = None
    basic_handwashing_facilities: Optional[float] = None
    safely_managed_drinking_water_services: Optional[float] = None
    diabetes_prevalence: Optional[float] = None


class EnvironmentIndicatorUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    energy_use: Optional[float] = None
    access_to_electricity: Optional[float] = None
    alternative_and_nuclear_energy: Optional[float] = None
    permanent_cropland: Optional[float] = None
    crop_production_index: Optional[float] = None
    gdp_per_unit_of_energy_use: Optional[float] = None
