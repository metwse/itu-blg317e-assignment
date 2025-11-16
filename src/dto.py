from src.entities import Continent

from typing import Optional
from pydantic import BaseModel, ConfigDict


class CountryUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: Optional[str] = None
    continent: Optional[Continent] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
