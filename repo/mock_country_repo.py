from typing import Any, Dict, List, Optional
import asyncio


class MockCountryRepo:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            return dict(row) if (row := self._store.get(code.strip().upper())) else None

    async def list_countries(self, limit: int = 100) -> List[Dict[str, Any]]:
        async with self._lock:
            return [dict(i) for i in list(self._store.values())[:limit]]

    async def insert_country(self, code: str, name: str) -> str:
        code = code.strip().upper()
        async with self._lock:
            if code in self._store:
                raise ValueError(f"country with code {code} already exists")
            self._store[code] = {"code": code, "name": name}
            return "INSERT 0 1"
