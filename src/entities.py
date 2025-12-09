from typing import Optional, Literal
from pydantic import BaseModel


Region = Literal[
    "Europe & Central Asia",
    "Middle East & North Africa",
    "South Asia",
    "Latin America & Caribbean",
    "Sub-Saharan Africa",
    "East Asia & Pacific",
    "North America"
]


class Provider(BaseModel):
    id: int
    email: str
    name: str
    password_hash: str
    nologin: bool
    is_admin: bool


class Economy(BaseModel):
    code: str
    name: str
    region: Optional[Region] = None


class Permission(BaseModel):
    provider_id: int
    economy_code: str
    year_start: int
    year_end: int


class HealthIndicator(BaseModel):
    provider_id: int
    economy_code: str
    year: int
    community_health_workers: Optional[int]
    prevalence_of_undernourishment: Optional[float]
    prevalence_of_severe_food_insecurity: Optional[float]
    basic_handwashing_facilities: Optional[float]
    safely_managed_drinking_water_services: Optional[float]
    diabetes_prevalence: Optional[float]


class EconomicIndicator(BaseModel):
    provider_id: int
    economy_code: str
    year: int
    industry: Optional[float]
    gdp_per_capita: Optional[float]
    trade: Optional[float]
    agriculture_forestry_and_fishing: Optional[float]


class EnvironmentIndicator(BaseModel):
    provider_id: int
    economy_code: str
    year: int
    energy_use: Optional[float]
    access_to_electricity: Optional[float]
    alternative_and_nuclear_energy: Optional[float]
    permanent_cropland: Optional[float]
    crop_production_index: Optional[float]
    gdp_per_unit_of_energy_use: Optional[float]
