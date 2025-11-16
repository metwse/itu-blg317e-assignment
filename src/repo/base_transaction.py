from typing import Any, Generic, List, Optional, Type, TypeVar
import asyncpg

T = TypeVar("T", bound=object)


# database access layer abstraction
class BaseTransaction(Generic[T]):
    def __init__(self, pool: asyncpg.pool.Pool, model: Type[T]):
        self.pool = pool
        self.model = model

    async def fetch(self, query: str, *args: Any) -> List[T]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [self.model(**row) for row in rows]

    async def fetchrow(self, query: str, *args: Any) -> Optional[T]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            if row is not None:
                return self.model(**row)
            else:
                return None

    async def fetchrow_raw(self, query: str, *args: Any) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            if row is not None:
                return dict(row)
            else:
                return None

    async def execute(self, query: str, *args: Any) -> str:
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
