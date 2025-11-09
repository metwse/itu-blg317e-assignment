import asyncio
from typing import Dict, Optional
from .state_model import CountryState


class StateManager:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._countries: Dict[str, CountryState] = {}

    async def get_country(self, code: str) -> Optional[CountryState]:
        async with self._lock:
            return self._countries.get(code.strip().upper())

    async def set_country(self, code: str, data: Dict) -> None:
        code = code.strip().upper()
        async with self._lock:
            self._countries[code] = CountryState(code=code, data=data)

    async def clear(self) -> None:
        async with self._lock:
            self._countries.clear()
