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
    """A generic repository implementing CRUD operations with dynamic SQL
    generation.

    This class uses Pydantic model to automatically generate common SQL queries
    for standard operations (INSERT, UPDATE, SELECT), reducing boilerplate code
    for each specific entity.

    This methods generally used for internal database management.
    """

    def __init__(self, pool: asyncpg.pool.Pool,
                 table_name: str, key_columns: List[str],
                 model_types: Tuple[Type[T], Type[U], Type[C]]):
        """Initialize the repository and pre-calculate SQL fragments.

        The constructor performs runtime introspection of the provided Pydantic
        models to build the SQL strings once, rather than rebuilding them
        on every query.
        """

        super().__init__(pool, model_types[0])

        self.table_name = table_name
        self.pool = pool

        # Extract column names from the CreateDTO (C) to ensure we only insert
        # valid fields
        columns = model_types[2].model_fields.keys()

        self.columns = ','.join(columns)
        self.key_columns = ','.join(key_columns)

        self.key_column_count = len(key_columns)
        # Pre-build the WHERE clause for PK lookups:
        # "id = $1" or "id = $1 AND code = $2"
        self.key_where_clauses = ' AND '.join([
            f"{key_columns[i]} = ${i + 1}"
            for i in range(len(key_columns))
        ])

        # Pre-build insert placeholders: "$1, $2, $3..."
        self.insert_placeholders = ','.join([
            f"${i + 1}"
            for i in range(len(columns))
        ])

        self.model_types = model_types

    async def get_by_keys(self, keys: List[Any]) -> Optional[T]:
        """Fetch a single entity by its primary key(s).

        Args:
            keys: A list of values corresponding to the `key_columns`.
                  Order must match the `key_columns` list provided in __init__.

        Returns:
            Optional[T]: The entity instance if found, otherwise None.
        """

        row = await self.fetchrow(
            f"""
            SELECT * FROM {self.table_name}
                WHERE {self.key_where_clauses}
            """,
            *keys
        )

        return row

    async def list(self, limit, offset) -> List[T]:
        """Fetch a paginated list of entities.

        Args:
            limit: Maximum number of records to return.
            offset: Number of records to skip.

        Returns:
            List[T]: A list of entity instances.
        """

        return await self.fetch(
            f"SELECT * FROM {self.table_name} LIMIT $1 OFFSET $2",
            limit, offset
        )

    async def insert(self, record: C) -> Optional[dict]:
        """Insert a new record into the database.

        Args:
            record (C): The CreateDTO containing the data to insert.

        Returns:
            Optional[dict]: The primary keys of the inserted record (via
                            RETURNING clause).
        """

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
        """Dynamically update specific fields of a record.

        This method supports partial updates. It only generates SQL SET clauses
        for fields that are explicitly set in the `update_dto`.

        Args:
            keys: The primary key(s) of the record to update.
            update_dto: The UpdateDTO containing only the fields to change.

        Returns:
            Optional[dict]: The primary keys of the updated record, or None if
                            no fields were provided to update.
        """

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
        """Delete a record by its primary keys.

        Args:
            keys: The primary key(s) of the record to delete.

        Returns:
            Optional[dict]: The primary keys of the deleted record.
        """

        return await self.fetchrow_raw(
            f"""
            DELETE FROM {self.table_name}
            WHERE {self.key_where_clauses}
            RETURNING {self.key_columns}
            """,
            *keys
        )

    async def truncate_cascade(self) -> str:
        """Reset table, cascading foreign keys."""

        return await self.execute(
            f"""
            TRUNCATE TABLE {self.table_name}
                RESTART IDENTITY
                CASCADE
            """
        )
