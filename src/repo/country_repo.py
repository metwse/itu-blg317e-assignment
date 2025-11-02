from typing import Any, Dict, List, Optional
from .base_repo import BaseRepo


class CountryRepo(BaseRepo):
    async def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        code_array = list(code.strip().upper())
        row = await self.fetchrow("SELECT * FROM countries WHERE code = $1", code_array)
        if not row:
            return None
        result = dict(row)
        result['code'] = ''.join(result['code'])
        return result

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        rows = await self.fetch("SELECT * FROM countries LIMIT $1", limit)
        result = []
        for r in rows:
            d = dict(r)
            d['code'] = ''.join(d['code'])
            result.append(d)
        return result

    async def insert_country(self, code: str, name: str, continent: Optional[str] = None,
                             lat: Optional[float] = None, lng: Optional[float] = None) -> str:
        code_array = list(code.strip().upper()[:3])
        return await self.execute(
            "INSERT INTO countries (code, name, continent, lat, lng) VALUES ($1, $2, $3, $4, $5)",
            code_array, name, continent, lat, lng)
