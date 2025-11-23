from typing import Optional, Literal
from pydantic import BaseModel


Continent = Literal[
    "Asia",
    "Europe",
    "North America",
    "South America",
    "Africa",
    "Oceania",
]


class Provider(BaseModel):
    id: int
    email: str
    name: str
    password_hash: str
    nologin: bool
    is_admin: bool


class Country(BaseModel):
    code: str
    name: str
    continent: Optional[Continent] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class Permission(BaseModel):
    provider_id: int
    country_code: str
    year_start: int
    year_end: int


class EconomicIndicator(BaseModel):
    provider_id: int
    country_code: str
    year: int
    industry: Optional[float]
    gdp_per_capita: Optional[str]
    trade: Optional[float]
    agriculture_forestry_and_fishing: Optional[float]


class HealthIndicator(BaseModel):
    provider_id: int
    country_code: str
    year: int
    community_health_workers: Optional[int]
    prevalence_of_undernourishment: Optional[float]
    prevalence_of_severe_food_insecurity: Optional[float]
    basic_handwashing_facilities: Optional[float]
    safely_managed_drinking_water_services: Optional[float]
    diabetes_prevalence: Optional[float]


class EnvironmentIndicator(BaseModel):
    provider_id: int
    country_code: str
    year: int
    energy_use: Optional[float]
    access_to_electricity: Optional[float]
    alternative_and_nuclear_energy: Optional[float]
    permanent_cropland: Optional[float]
    crop_production_index: Optional[float]
    gdp_per_unit_of_energy_use: Optional[str]
