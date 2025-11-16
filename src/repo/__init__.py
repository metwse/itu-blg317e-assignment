from .base_repo import BaseRepo

from src.dto import CountryUpdateDto
from src.entities import Country


class CountryRepo(BaseRepo[Country, CountryUpdateDto, Country]):
    def __init__(self, pool):
        super().__init__(pool, 'countries', ['code'],
                         (Country, CountryUpdateDto, Country))


__all__ = ["CountryRepo"]
