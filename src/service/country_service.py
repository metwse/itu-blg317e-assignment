from typing import Any, Dict, List, Optional
from ..repo.country_repo import CountryRepo

VALID_CONTINENTS = {'Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania'}


class CountryService:
    def __init__(self, repo: CountryRepo):
        self.repo = repo

    async def get_country(self, code: str) -> Optional[Dict[str, Any]]:
        return await self.repo.get_by_code(code.strip().upper()) if code else None

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.repo.list_countries(limit)

    async def create_country(self, code: str, name: str, continent: Optional[str] = None,
                             lat: Optional[float] = None, lng: Optional[float] = None) -> str:
        c, n = code.strip().upper(), name.strip()
        if not c or not n:
            raise ValueError("code and name are required")
        if continent and continent not in VALID_CONTINENTS:
            raise ValueError(f"continent must be one of {VALID_CONTINENTS}")
        return await self.repo.insert_country(c, n, continent, lat, lng)
