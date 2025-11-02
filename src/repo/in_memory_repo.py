"""In-memory repository implementation for testing without database."""
from typing import Any, Dict, List, Optional
import asyncio


class InMemoryRepo:
    """In-memory repository that implements the same interface as CountryRepo."""

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            return dict(row) if (row := self._store.get(code.strip().upper())) else None

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        async with self._lock:
            return [dict(i) for i in list(self._store.values())[:limit]]

    async def insert_country(self, code: str, name: str, continent: Optional[str] = None,
                             lat: Optional[float] = None, lng: Optional[float] = None) -> str:
        code = code.strip().upper()[:3]
        async with self._lock:
            if code in self._store:
                raise ValueError(f"country with code {code} already exists")
            self._store[code] = {"code": code, "name": name, "continent": continent, "lat": lat, "lng": lng}
            return "INSERT 0 1"
