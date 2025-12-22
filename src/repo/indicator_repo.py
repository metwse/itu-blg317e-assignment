from . import BaseRepo

from src.dto import IndicatorCreateDto, IndicatorUpdateDto
from src.entities import Indicator


class IndicatorRepo(BaseRepo):
    """Repository that operates over three physical indicator tables:
    `economic_indicators`, `health_indicators`, `environment_indicators`.

    The public API (get_indicator, upsert_indicator) remains unchanged and
    returns/accepts the same combined record shape as before.
    """

    def __init__(self, pool):
        # Keep BaseRepo initialized for helper methods. Table name here is
        # informational only; we won't rely on BaseRepo's single-table
        # insert/update for indicators anymore.
        super().__init__(pool, 'indicators',
                         ['provider_id', 'economy_code', 'year'],
                         (Indicator, IndicatorUpdateDto, IndicatorCreateDto))

    async def get_indicator(self, provider_id: int, economy_code: str,
                            year: int):  # PORTAL
        """Fetch combined indicator data for a specific economy/year across
        the three indicator tables. Returns merged dict or None.
        """
        # Fetch rows from each table and merge results in Python for clarity.
        econ = await self.fetchrow_raw(
            "SELECT * FROM economic_indicators WHERE provider_id = $1 "
            "AND economy_code = $2 AND year = $3",
            provider_id, economy_code, year
        )
        health = await self.fetchrow_raw(
            "SELECT * FROM health_indicators WHERE provider_id = $1 "
            "AND economy_code = $2 AND year = $3",
            provider_id, economy_code, year
        )
        env = await self.fetchrow_raw(
            "SELECT * FROM environment_indicators WHERE provider_id = $1 "
            "AND economy_code = $2 AND year = $3",
            provider_id, economy_code, year
        )

        if not (econ or health or env):
            return None

        # Start with the composite key fields
        result = {
            'provider_id': provider_id,
            'economy_code': economy_code,
            'year': year
        }

        # Merge non-key fields from each table (later tables overwrite earlier
        # ones for identical keys, but they are disjoint by design)
        for part in (econ, health, env):
            if part:
                for k, v in part.items():
                    if k in ('provider_id', 'economy_code', 'year'):
                        continue
                    result[k] = v

        return result

    async def upsert_indicator(self, provider_id: int, economy_code: str,
                               year: int, data: dict):  # PORTAL
        """Insert or update indicator data across the three tables.

        The `data` dict may contain any subset of economic, health, or
        environment fields. Only the relevant tables are touched. Returns a
        combined result dict and `was_created` boolean that is True if any of
        the affected tables created a new row.
        """
        economic_fields = [
            'industry', 'gdp_per_capita', 'trade',
            'agriculture_forestry_and_fishing'
        ]
        health_fields = [
            'community_health_workers',
            'prevalence_of_undernourishment',
            'prevalence_of_severe_food_insecurity',
            'basic_handwashing_facilities',
            'safely_managed_drinking_water_services',
            'diabetes_prevalence'
        ]
        environment_fields = [
            'energy_use', 'access_to_electricity',
            'alternative_and_nuclear_energy',
            'permanent_cropland', 'crop_production_index',
            'gdp_per_unit_of_energy_use'
        ]

        created_any = False
        performed_any = False

        async def _upsert_group(table_name, fields):
            nonlocal created_any, performed_any
            cols = ['provider_id', 'economy_code', 'year'] + fields
            values = [provider_id, economy_code, year] + \
                [data.get(f) for f in fields]

            # If all provided values for the group are None/absent, skip
            if all(v is None for v in values[3:]):
                return

            performed_any = True

            placeholders = ', '.join([f"${i + 1}" for i in range(len(values))])
            cols_str = ', '.join(cols)
            update_clause = ', '.join([f"{f} = EXCLUDED.{f}" for f in fields])

            query = f"""
                INSERT INTO {table_name} ({cols_str})
                VALUES ({placeholders})
                ON CONFLICT (provider_id, economy_code, year)
                DO UPDATE SET {update_clause}
                RETURNING (xmax = 0) AS was_created
            """

            res = await self.fetchrow_raw(query, *values)
            if res and res.get('was_created'):
                created_any = True

        # Upsert per logical group
        await _upsert_group('economic_indicators', economic_fields)
        await _upsert_group('health_indicators', health_fields)
        await _upsert_group('environment_indicators', environment_fields)

        # Preserve previous behaviour: if client provided no indicator fields
        # at all, create a minimal row in `economic_indicators` so a record
        # exists.
        if not performed_any:
            res = await self.fetchrow_raw(
                """
                INSERT INTO economic_indicators (provider_id, economy_code,
                                                 year)
                VALUES ($1, $2, $3)
                ON CONFLICT (provider_id, economy_code, year) DO NOTHING
                RETURNING (xmax = 0) AS was_created
                """,
                provider_id, economy_code, year
            )
            if res and res.get('was_created'):
                created_any = True

        # Return the merged record and whether anything was created
        result = await self.get_indicator(provider_id, economy_code, year)
        return result, created_any

    # --- Override BaseRepo CRUD methods that would otherwise act on the
    #     non-existent single `indicators` table. These implementations operate
    #     on the three concrete tables and preserve the BaseRepo public
    #     contracts (return the primary key dict or model instance where
    #     appropriate).

    async def insert(self, record: IndicatorCreateDto):
        """Insert a new indicator record by distributing provided fields to
        the appropriate tables. Returns the key columns dict on success.
        """
        payload = record.model_dump()
        provider_id = payload.pop('provider_id')
        economy_code = payload.pop('economy_code')
        year = payload.pop('year')

        # Use upsert_indicator logic to ensure rows are created in the
        # corresponding category tables.
        await self.upsert_indicator(provider_id, economy_code, year, payload)

        return {
            'provider_id': provider_id,
            'economy_code': economy_code,
            'year': year
        }

    async def get_by_keys(self, keys: list):
        """Return an Indicator model instance for the provided primary keys."""
        provider_id, economy_code, year = keys
        data = await self.get_indicator(provider_id, economy_code, year)
        if data is None:
            return None
        # Build the Indicator entity
        return self.model(**data)

    async def update(self, keys: list, update_dto: IndicatorUpdateDto):
        """Update only provided fields in their respective category tables.
        Returns the key dict if any update occurred, otherwise None.
        """
        fields_to_update = update_dto.model_dump(exclude_unset=True)
        if not fields_to_update:
            return None

        provider_id, economy_code, year = keys

        economic_fields = {
            'industry', 'gdp_per_capita', 'trade',
            'agriculture_forestry_and_fishing'
        }
        health_fields = {
            'community_health_workers',
            'prevalence_of_undernourishment',
            'prevalence_of_severe_food_insecurity',
            'basic_handwashing_facilities',
            'safely_managed_drinking_water_services',
            'diabetes_prevalence'
        }
        environment_fields = {
            'energy_use', 'access_to_electricity',
            'alternative_and_nuclear_energy',
            'permanent_cropland', 'crop_production_index',
            'gdp_per_unit_of_energy_use'
        }

        updates = {
            'economic_indicators': {k: v for k, v in fields_to_update.items() if k in economic_fields},
            'health_indicators': {k: v for k, v in fields_to_update.items() if k in health_fields},
            'environment_indicators': {k: v for k, v in fields_to_update.items() if k in environment_fields}
        }

        any_updated = False
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for table, cols in updates.items():
                    if not cols:
                        continue
                    set_clause = ', '.join([f"{c} = ${i + 4}" for i, c in enumerate(cols.keys())])
                    # param ordering: provider_id, economy_code, year, <values...>
                    params = [provider_id, economy_code, year, *cols.values()]
                    query = f"""
                        UPDATE {table}
                        SET {set_clause}
                        WHERE provider_id = $1 AND economy_code = $2 AND year = $3
                        RETURNING provider_id, economy_code, year
                    """
                    row = await conn.fetchrow(query, *params)
                    if row:
                        any_updated = True

        if any_updated:
            return {
                'provider_id': provider_id,
                'economy_code': economy_code,
                'year': year
            }
        return None

    async def delete(self, keys: list):
        provider_id, economy_code, year = keys
        deleted_any = False

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for table in ('economic_indicators', 'health_indicators', 'environment_indicators'):
                    row = await conn.fetchrow(
                        f"""
                        DELETE FROM {table}
                        WHERE provider_id = $1 AND economy_code = $2 AND year = $3
                        RETURNING provider_id, economy_code, year
                        """,
                        provider_id, economy_code, year
                    )
                    if row:
                        deleted_any = True

        if deleted_any:
            return {
                'provider_id': provider_id,
                'economy_code': economy_code,
                'year': year
            }
        return None

    async def truncate_cascade(self) -> str:
        """Truncate all three indicator tables."""
        return await self.execute(
            """
            TRUNCATE TABLE economic_indicators, health_indicators, environment_indicators
                RESTART IDENTITY
                CASCADE
            """
        )
