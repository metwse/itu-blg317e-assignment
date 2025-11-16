from src.repo import CountryRepo
from src.entities import Country

from typing import List, Optional


class CountryService:
    def __init__(self, pool):
        self.repo = CountryRepo(pool)

    async def get_country(self, code: str) -> Optional[Country]:
        return await self.repo.get_by_id(code.strip().upper())

    async def list_countries(self, limit, offset) \
            -> List[Country]:
        return await self.repo.list(limit, offset)

    async def create_country(self, country) -> str:
        return await self.repo.insert(country)

    async def update_country(self, code, update_dto) -> str | None:
        return await self.repo.update(code, update_dto)

    async def delete_country(self, code) -> str:
        return await self.repo.delete(code)
