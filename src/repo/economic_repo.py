from typing import List, Optional
from src.entities import EconomicIndicator
from src.repo.base_repo import BaseRepo

class EconomicIndicatorRepo(BaseRepo[EconomicIndicator]):
    def __init__(self, pool):
        super().__init__(pool, EconomicIndicator)

    async def list_by_country(self, provider_id: int, code: str) -> List[EconomicIndicator]:
        query = """
            SELECT provider_id, country_code, year,
                   industry, gdp_per_capita, trade,
                   agriculture_forestry_and_fishing
            FROM economic_indicators
            WHERE provider_id = $1 AND country_code = $2
            ORDER BY year;
        """
        rows = await self.fetch(query, provider_id, code.strip().upper())
        return rows

    async def insert_indicator(self, indicator: EconomicIndicator) -> str:
        query = """
            INSERT INTO economic_indicators
                (provider_id, country_code, year,
                 industry, gdp_per_capita, trade,
                 agriculture_forestry_and_fishing)
            VALUES ($1, $2, $3, $4, $5, $6, $7);
        """
        await self.execute(
            query,
            indicator.provider_id,
            indicator.country_code,
            indicator.year,
            indicator.industry,
            indicator.gdp_per_capita,
            indicator.trade,
            indicator.agriculture_forestry_and_fishing,
        )
        return "Inserted"
