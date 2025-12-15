"""Domain Entities (Database Models).

This module defines the core data structures that map directly to the
PostgreSQL database tables. These Pydantic models represent the "Truth" of the
data as it exists in storage.

Usage in Architecture:
    These models correspond to the Generic Type `T` in `BaseRepo[T, U, C]`.
    They are primarily used for:
    1. Parsing rows returned by `asyncpg` (SELECT queries).
    2. Type hinting the return values of Service and Repository 'get' methods.
    3. Serializing the final JSON response sent to the client.
"""

from typing import Optional, Literal
from pydantic import BaseModel


Region = Literal[
    "East Asia & Pacific",
    "Europe & Central Asia",
    "Latin America & Caribbean",
    "Middle East, North Africa, Afghanistan & Pakistan",
    "North America",
    "South Asia",
    "Sub-Saharan Africa"
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
    community_health_workers: Optional[float]
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
