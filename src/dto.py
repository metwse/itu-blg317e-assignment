from src.entities import Continent

from typing import Optional
from pydantic import BaseModel, ConfigDict


class CountryUpdateDto(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: Optional[str]
    continent: Optional[Continent]
    lat: Optional[float]
    lng: Optional[float]
