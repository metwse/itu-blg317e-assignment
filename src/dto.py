"""Data Transfer Objects (DTOs).

This module defines the Pydantic models used strictly for data create and
update operations. These models decouple the internal database schema from the
external API interface.

Usage in Architecture:
    These models correspond to Generic Types `U` and `C` in
    `BaseRepo[T, U, C]`.

    1. **CreateDto (C):**
       - Used for POST requests.
       - Contains all fields required to create a new record.
       - Excludes auto-generated fields (like SERIAL).

    2. **UpdateDto (U):**
       - Used for PATCH requests.
       - All fields are `Optional` to allow partial updates.
       - Uses `model_config = ConfigDict(extra='ignore')` to safely ignore
         extraneous fields sent by clients without raising validation errors.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


# 1. Provider DTOs
# ---------------------------------------------------------
class ProviderUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    administrative_account: Optional[int] = None
    technical_account: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    nologin: Optional[bool] = None


class ProviderCreateDto(BaseModel):
    administrative_account: int
    technical_account: Optional[int] = None
    name: str
    description: Optional[str] = None
    website_url: Optional[str] = None
    nologin: bool


# 3. User DTOs
# ---------------------------------------------------------
class UserUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None


class UserCreateDto(BaseModel):
    email: str
    password: str
    name: str


# 3. Economy DTOs
# ---------------------------------------------------------
class EconomyUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: Optional[str] = None
    region: Optional[str] = Field(None, max_length=3)
    income_level: Optional[str] = Field(None, max_length=3)
    is_aggregate: Optional[bool] = None
    capital_city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class EconomyCreateDto(BaseModel):
    code: str = Field(..., max_length=3)
    name: str
    region: Optional[str] = Field(None, max_length=3)
    income_level: Optional[str] = Field(None, max_length=3)
    is_aggregate: bool
    capital_city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


# 4. Permission DTOs
# ---------------------------------------------------------
class PermissionUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    year_start: Optional[int] = None
    year_end: Optional[int] = None
    footnote: Optional[str] = None


class PermissionCreateDto(BaseModel):
    provider_id: int
    year_start: int
    year_end: int
    footnote: Optional[str] = None

    economy_code: Optional[str] = Field(None, max_length=3)
    region: Optional[str] = Field(None, max_length=3)

    @model_validator(mode='after')
    def check_scope_xor(self):
        has_economy = self.economy_code is not None
        has_region = self.region is not None

        if has_economy == has_region:
            raise ValueError("Permission must specify either 'economy_code' "
                             "or 'region', but not both.")
        return self


# 5. Indicator DTOs
# ---------------------------------------------------------
class IndicatorUpdateDto(BaseModel):
    """Used for PATCH requests.
    Clients can send any subset of Economic, Health, or Environment fields.
    """
    model_config = ConfigDict(extra='ignore')

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


class IndicatorCreateDto(IndicatorUpdateDto):
    """Used for POST requests.
    Inherits all fields from UpdateDto since all indicator values are nullable,
    but requires the composite key fields.
    """
    provider_id: int
    economy_code: str = Field(..., max_length=3)
    year: int
