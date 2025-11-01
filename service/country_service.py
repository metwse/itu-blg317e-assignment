from typing import Any, Dict, List, Optional
from repo.country_repo import CountryRepo


class CountryService:
    def __init__(self, repo: CountryRepo):
        self.repo = repo

    async def get_country(self, code: str) -> Optional[Dict[str, Any]]:
        return await self.repo.get_by_code(code.strip().upper()) if code else None

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.repo.list_countries(limit)

    async def create_country(self, code: str, name: str) -> str:
        c, n = code.strip().upper(), name.strip()
        if not c or not n:
            raise ValueError("code and name are required")
        return await self.repo.insert_country(c, n)
