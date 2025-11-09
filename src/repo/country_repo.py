from typing import Any, Dict, List, Optional
from .base_repo import BaseRepo


class CountryRepo(BaseRepo):
    async def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        row = await self.fetchrow("SELECT * FROM countries WHERE code = $1", code.strip().upper())
        return dict(row) if row else None

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        return [dict(r) for r in await self.fetch("SELECT * FROM countries LIMIT $1", limit)]

    async def insert_country(self, code: str, name: str, continent: Optional[str] = None,
                             lat: Optional[float] = None, lng: Optional[float] = None) -> str:
        return await self.execute(
            "INSERT INTO countries (code, name, continent, lat, lng) VALUES ($1, $2, $3, $4, $5)",
            code.strip().upper()[:3], name, continent, lat, lng)
