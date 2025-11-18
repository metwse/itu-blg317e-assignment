from src.entities import Continent

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


class CountryUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: Optional[str] = None
    continent: Optional[Continent] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class PermissionUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    year_start: Optional[int] = None
    year_end: Optional[int] = None
