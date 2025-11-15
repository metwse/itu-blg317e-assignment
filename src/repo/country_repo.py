from .base_repo import BaseRepo

from src.entities import Country

from typing import List, Optional


class CountryRepo(BaseRepo[Country]):
    def __init__(self, pool):
        super().__init__(pool, Country)

    async def get_by_code(self, code: str) -> Optional[Country]:
        row = await self.fetchrow(
            """
            SELECT * FROM countries
                WHERE code = $1
            """, code.strip().upper()
        )

        return row

    async def list_countries(self, limit: int = 100, offset: int = 0) \
            -> List[Country]:
        return await self.fetch(
            "SELECT * FROM countries LIMIT $1 OFFSET $2", limit, offset
        )

    async def insert_country(self, country: Country) -> str:
        country_dict = country.model_dump()

        return await self.execute(
            """
            INSERT INTO countries (code, name, continent, lat, lng)
                VALUES ($1, $2, $3, $4, $5)
            """,
            country_dict["code"].upper(), country_dict["name"],
            country_dict["continent"], country_dict["lat"], country_dict["lng"]
        )
