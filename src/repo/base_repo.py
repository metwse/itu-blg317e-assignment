from src.repo.base_transaction import BaseTransaction

from pydantic import BaseModel
from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar

import asyncpg


T = TypeVar('T', bound=BaseModel)  # underlying entity
U = TypeVar('U', bound=BaseModel)  # DTO for updatable fields of the entity
C = TypeVar('C', bound=BaseModel)  # DTO for creating new entity


# ORM mappings for database entities
class BaseRepo(Generic[T, U, C],
               BaseTransaction[T]):
    def __init__(self, pool: asyncpg.pool.Pool,
                 table_name: str, key_columns: List[str],
                 model_types: Tuple[Type[T], Type[U], Type[C]]):
        super().__init__(pool, model_types[0])

        self.table_name = table_name
        self.pool = pool

        columns = model_types[0].model_fields.keys()

        self.columns = ','.join(columns)
        self.key_columns = ','.join(key_columns)

        self.key_column_count = len(key_columns)
        self.key_where_clauses = ' AND '.join([
            f"{key_columns[i]} = ${i + 1}"
            for i in range(len(key_columns))
        ])

        self.insert_placeholders = ','.join([
            f"${i + 1}"
            for i in range(len(columns))
        ])

    async def get_by_keys(self, keys: List[Any]) -> Optional[T]:
        row = await self.fetchrow(
            f"""
            SELECT {self.columns} FROM {self.table_name}
                WHERE {self.key_where_clauses}
            """, *keys
        )

        return row

    async def list(self, limit, offset) \
            -> List[T]:
        return await self.fetch(
            f"SELECT * FROM {self.table_name} LIMIT $1 OFFSET $2",
            limit, offset
        )

    async def insert(self, record: C) -> Optional[dict]:
        model_dump = record.model_dump()

        return await self.fetchrow_raw(
            f"""
            INSERT INTO {self.table_name} ({self.columns})
                VALUES ({self.insert_placeholders})
                RETURNING {self.key_columns}
            """,
            *list(model_dump.values())
        )

    async def update(self, keys: List[Any], update_dto: U) \
            -> Optional[dict]:
        fields_to_update = update_dto.model_dump(exclude_unset=True)

        set_clauses = []
        update_values = []

        placeholder_start_index = self.key_column_count + 1
        for i, (column, value) in \
                enumerate(fields_to_update.items(),
                          start=placeholder_start_index):
            set_clauses.append(f"{column} = ${i}")
            update_values.append(value)

        if len(set_clauses) == 0:
            return None

        return await self.fetchrow_raw(
            f"""
            UPDATE {self.table_name}
            SET {','.join(set_clauses)}
            WHERE {self.key_where_clauses}
            RETURNING {self.key_columns}
            """,
            *keys, *update_values
        )

    async def delete(self, keys: List[Any]) -> Optional[dict]:
        return await self.fetchrow_raw(
            f"""
            DELETE FROM {self.table_name}
            WHERE {self.key_where_clauses}
            RETURNING {self.key_columns}
            """,
            *keys
        )
