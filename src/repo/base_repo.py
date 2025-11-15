from typing import Any, Generic, List, Optional, Type, TypeVar, cast
import asyncpg

T = TypeVar("T", bound=object)


# database access layer abstraction
class BaseRepo(Generic[T]):
    def __init__(self, pool: asyncpg.pool.Pool, _: Type[T]):
        self.pool = pool

    async def fetch(self, query: str, *args: Any) -> List[T]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [cast(T, dict(r)) for r in rows]

    async def fetchrow(self, query: str, *args: Any) -> Optional[T]:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query: str, *args: Any) -> str:
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
