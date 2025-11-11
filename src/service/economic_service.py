from typing import List
from src.entities import EconomicIndicator
from src.repo.economic_repo import EconomicIndicatorRepo

class EconomicService:
    def __init__(self, repo: EconomicIndicatorRepo):
        self._repo = repo

    async def list_indicators(self, provider_id: int, code: str) -> List[EconomicIndicator]:
        return await self._repo.list_by_country(provider_id, code)

    async def create_indicator(self, indicator: EconomicIndicator) -> str:
        return await self._repo.insert_indicator(indicator)
