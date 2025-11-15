from src.repo.country_repo import CountryRepo
from src.entities import Country

from typing import List, Optional


class CountryService:
    def __init__(self, pool):
        self.repo = CountryRepo(pool)

    async def get_country(self, code: str) -> Optional[Country]:
        return await self.repo.get_by_code(code.strip().upper())

    async def list_countries(self, limit: int = 100, offset: int = 0) \
            -> List[Country]:
        return await self.repo.list_countries(limit, offset)

    async def create_country(self, country: Country) -> str:
        return await self.repo.insert_country(country)
