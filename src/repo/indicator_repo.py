from . import BaseRepo

from src.dto import IndicatorCreateDto, IndicatorUpdateDto
from src.entities import Indicator


class IndicatorRepo(BaseRepo):
    def __init__(self, pool):
        super().__init__(pool, 'indicators',
                         ['provider_id', 'economy_code', 'year'],
                         (Indicator, IndicatorUpdateDto, IndicatorCreateDto))

    async def get_indicator(self, provider_id: int, economy_code: str,
                            year: int):  # PORTAL
        """Fetch existing indicator data for a specific economy/year.

        Args:
            provider_id: The provider's ID.
            economy_code: The economy code (e.g., 'TUR').
            year: The year.

        Returns:
            The indicator record if found, None otherwise.
        """
        return await self.fetchrow_raw(
            """
            SELECT * FROM indicators
            WHERE provider_id = $1 AND economy_code = $2 AND year = $3
            """,
            provider_id, economy_code, year
        )

    async def upsert_indicator(self, provider_id: int, economy_code: str,
                               year: int, data: dict):  # PORTAL
        """Insert or update indicator data using ON CONFLICT DO UPDATE.

        Only updates non-null fields provided in the data dict (partial
        update).

        Args:
            provider_id: The provider's ID.
            economy_code: The economy code (e.g., 'TUR').
            year: The year.
            data: Dict containing indicator field values to set.

        Returns:
            Tuple of (result_dict, was_created: bool).
        """
        # All possible indicator fields (excluding composite key fields)
        indicator_fields = [
            'industry', 'gdp_per_capita', 'trade',
            'agriculture_forestry_and_fishing',
            'community_health_workers',
            'prevalence_of_undernourishment',
            'prevalence_of_severe_food_insecurity',
            'basic_handwashing_facilities',
            'safely_managed_drinking_water_services',
            'diabetes_prevalence',
            'energy_use', 'access_to_electricity',
            'alternative_and_nuclear_energy',
            'permanent_cropland', 'crop_production_index',
            'gdp_per_unit_of_energy_use'
        ]

        # Build SET clause for UPDATE: only include non-null fields from data
        update_parts = []
        for field in indicator_fields:
            if field in data and data[field] is not None:
                update_parts.append(
                    f"{field} = EXCLUDED.{field}"
                )

        # If no fields to update, just do an insert that ignores conflicts
        if not update_parts:
            update_clause = "provider_id = EXCLUDED.provider_id"  # No-op
        else:
            update_clause = ", ".join(update_parts)

        # Build column list and values for INSERT
        columns = ['provider_id', 'economy_code', 'year'] + indicator_fields
        values = [provider_id, economy_code, year]
        for field in indicator_fields:
            values.append(data.get(field))

        placeholders = ", ".join([f"${i + 1}" for i in range(len(values))])
        columns_str = ", ".join(columns)

        query = f"""
            INSERT INTO indicators ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT (provider_id, economy_code, year)
            DO UPDATE SET {update_clause}
            RETURNING
                provider_id, economy_code, year,
                (xmax = 0) AS was_created
        """

        result = await self.fetchrow_raw(query, *values)

        if result:
            was_created = result.pop('was_created', False)
            return result, was_created
        return None, False
