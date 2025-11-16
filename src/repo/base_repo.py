from pydantic import BaseModel
from src.repo.base_translaction import BaseTranslaction

from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar
import asyncpg


T = TypeVar('T', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)


class BaseRepo(Generic[T, U], BaseTranslaction[T]):
    def __init__(self, pool: asyncpg.pool.Pool,
                 table_name: str, id_column: str,
                 Types: Tuple[Type[T], Type[U]]):
        super().__init__(pool, Types[0])

        self.table_name = table_name
        self.id_column = id_column
        self.pool = pool

        columns = Types[0].model_fields.keys()
        update_values = [f"${i + 1}" for i in range(len(columns))]

        self.columns = ','.join(columns)
        self.update_values = ','.join(update_values)

    async def get_by_id(self, id: Any) -> Optional[T]:
        row = await self.fetchrow(
            f"""
            SELECT * FROM {self.table_name}
                WHERE {self.id_column} = $1
            """, id
        )

        return row

    async def list_countries(self, limit, offset) \
            -> List[T]:
        return await self.fetch(
            f"SELECT * FROM {self.table_name} LIMIT $1 OFFSET $2",
            limit, offset
        )

    async def insert_countries(self, record: T) -> str:
        model_dump = record.model_dump()

        return await self.execute(
            f"""
            INSERT INTO {self.table_name} ({self.columns})
                VALUES ({self.update_values})
            """,
            *list(model_dump.values())
        )

    async def update_country(self, id: Any, update_dto: U) \
            -> str | None:
        fields_to_update = update_dto.model_dump(exclude_unset=True)

        set_clauses = []
        update_values = []

        i = 2
        for column, value in fields_to_update.items():
            if value is not None:
                set_clauses.append(f"{column} = ${i}")
                update_values.append(value)
                i += 1

        if len(set_clauses) == 0:
            return None

        return await self.execute(
            f"""
            UPDATE {self.table_name}
            SET {','.join(set_clauses)}
            WHERE {self.id_column} = $1
            """,
            id, *update_values
        )
