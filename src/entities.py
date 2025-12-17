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

from typing import Optional
from pydantic import BaseModel, Field, model_validator


# 1. Lookups (Regions & Income Levels)
# ---------------------------------------------------------
class Region(BaseModel):
    id: str = Field(..., max_length=3)
    name: str


class IncomeLevel(BaseModel):
    id: str = Field(..., max_length=3)
    name: str


# 2. Auth Entities (Provider & User)
# ---------------------------------------------------------
class User(BaseModel):
    id: int
    email: str
    password: str
    name: str


class Provider(BaseModel):
    id: int
    administrative_account: int
    technical_account: Optional[int] = None
    name: str
    description: Optional[str] = None
    nologin: bool


# 3. Core Entities (Economy & Permissions)
# ---------------------------------------------------------
class Economy(BaseModel):
    code: str = Field(..., max_length=3)
    name: str
    region: Optional[str] = Field(None, max_length=3)
    income_level: Optional[str] = Field(None, max_length=3)
    is_aggregate: bool
    capital_city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class Permission(BaseModel):
    id: int
    provider_id: int
    year_start: int
    year_end: int
    footnote: Optional[str] = None

    # Permission Scope (XOR)
    economy_code: Optional[str] = Field(None, max_length=3)
    region: Optional[str] = Field(None, max_length=3)

    @model_validator(mode='after')
    def check_scope_xor(self):
        """Permission must be for EITHER an economy OR a region, never both or
        neither.
        """
        has_economy = self.economy_code is not None
        has_region = self.region is not None

        if has_economy == has_region:
            raise ValueError("Permission must specify either 'economy_code' "
                             "or 'region', but not both.")
        return self


# 4. Indicator Entity
# ---------------------------------------------------------
class Indicator(BaseModel):
    provider_id: int
    economy_code: str
    year: int

    industry: Optional[float] = None
    gdp_per_capita: Optional[float] = None
    trade: Optional[float] = None
    agriculture_forestry_and_fishing: Optional[float] = None

    community_health_workers: Optional[float] = None
    prevalence_of_undernourishment: Optional[float] = None
    prevalence_of_severe_food_insecurity: Optional[float] = None
    basic_handwashing_facilities: Optional[float] = None
    safely_managed_drinking_water_services: Optional[float] = None
    diabetes_prevalence: Optional[float] = None

    energy_use: Optional[float] = None
    access_to_electricity: Optional[float] = None
    alternative_and_nuclear_energy: Optional[float] = None
    permanent_cropland: Optional[float] = None
    crop_production_index: Optional[float] = None
    gdp_per_unit_of_energy_use: Optional[float] = None
