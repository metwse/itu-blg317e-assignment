from typing import Any, Dict, List, Optional, Protocol


class CountryRepoProtocol(Protocol):
    async def get_by_code(self, code: str) -> Optional[Dict[str, Any]]: ...
    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]: ...
    async def insert_country(self, code: str, name: str, continent: Optional[str] = None,
                             lat: Optional[float] = None, lng: Optional[float] = None) -> str: ...


class CountryService:
    def __init__(self, repo: CountryRepoProtocol):
        self.repo = repo

    async def get_country(self, code: str) -> Optional[Dict[str, Any]]:
        return await self.repo.get_by_code(code.strip().upper()) if code else None

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.repo.list_countries(limit)

    async def create_country(self, code: str, name: str, continent: Optional[str] = None,
                             lat: Optional[float] = None, lng: Optional[float] = None) -> str:
        return await self.repo.insert_country(code.strip().upper(), name.strip(), continent, lat, lng)
