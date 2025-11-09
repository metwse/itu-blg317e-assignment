from typing import Any, Iterable
import asyncpg


# database access layer abstraction
class BaseRepo:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def fetch(self, query: str, *args: Any) -> Iterable[asyncpg.Record]:
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> Any:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query: str, *args: Any) -> str:
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
