"""Public repository for read-only data access with JOINs."""

from src.dto import IndicatorFilters

from typing import List, Tuple
import asyncpg


def build_indicator_filter_clause(
    filters: IndicatorFilters,
    extra_conditions: List[str] = []
) -> Tuple[str, List, int]:
    """Build WHERE clause and params from IndicatorFilters.

    Args:
        filters: The filter parameters.
        extra_conditions: Additional WHERE conditions (e.g., category filters).

    Returns:
        Tuple of (where_clause, params_list, next_param_index).
    """
    conditions = list(extra_conditions) if extra_conditions else []
    params = []
    param_idx = 1

    if filters.economy_code:
        conditions.append(f"i.economy_code = ${param_idx}")
        params.append(filters.economy_code.upper())
        param_idx += 1

    if filters.region:
        conditions.append(f"e.region = ${param_idx}")
        params.append(filters.region.upper())
        param_idx += 1

    if filters.year is not None:
        conditions.append(f"i.year = ${param_idx}")
        params.append(filters.year)
        param_idx += 1
    else:
        if filters.year_start is not None:
            conditions.append(f"i.year >= ${param_idx}")
            params.append(filters.year_start)
            param_idx += 1
        if filters.year_end is not None:
            conditions.append(f"i.year <= ${param_idx}")
            params.append(filters.year_end)
            param_idx += 1

    if filters.provider_id is not None:
        conditions.append(f"i.provider_id = ${param_idx}")
        params.append(filters.provider_id)
        param_idx += 1

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    return where_clause, params, param_idx


class PublicRepo:
    """Repository for public read-only queries with table joins.

    This repo handles all database access for the public API layer,
    providing pre-joined views of economies, indicators, and related data.
    """

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def list_economies(self) -> List[dict]:
        """List all economies with region and income level names."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT
                    e.code,
                    e.name,
                    e.is_aggregate,
                    e.capital_city,
                    e.lat,
                    e.lng,
                    r.id AS region_code,
                    r.name AS region_name,
                    i.id AS income_level_code,
                    i.name AS income_level_name
                FROM economies e
                LEFT JOIN regions r ON e.region = r.id
                LEFT JOIN income_levels i ON e.income_level = i.id
                ORDER BY e.name
            """)
            return [dict(row) for row in rows]

    async def list_regions(self) -> List[dict]:
        """List all regions."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM regions ORDER BY name")
            return [dict(row) for row in rows]

    async def list_income_levels(self) -> List[dict]:
        """List all income levels."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM income_levels ORDER BY name")
            return [dict(row) for row in rows]

    async def list_providers(self) -> List[dict]:
        """List all providers with admin/tech user names."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT
                    p.id,
                    p.name,
                    p.description,
                    p.website_url,
                    a.name AS admin_name,
                    t.name AS tech_name
                FROM providers p
                LEFT JOIN users a ON p.administrative_account = a.id
                LEFT JOIN users t ON p.technical_account = t.id
                WHERE p.immutable = false
                ORDER BY p.name
            """)
            return [dict(row) for row in rows]

    async def list_indicators(self, filters: IndicatorFilters) -> List[dict]:
        """List all indicators with economy and provider info.

        This query builds a combined set by FULL OUTER JOINing the three
        category tables and exposing the combined columns under alias `i`, so
        the existing filter builder continues to work.
        """
        where_clause, params, param_idx = build_indicator_filter_clause(filters)
        params.extend([filters.limit, filters.offset])

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT
                    i.provider_id,
                    p.name AS provider_name,
                    i.economy_code,
                    e.name AS economy_name,
                    r.name AS region_name,
                    il.name AS income_level_name,
                    i.year,
                    i.gdp_per_capita,
                    i.industry,
                    i.trade,
                    i.agriculture_forestry_and_fishing,
                    i.community_health_workers,
                    i.diabetes_prevalence,
                    i.prevalence_of_undernourishment,
                    i.prevalence_of_severe_food_insecurity,
                    i.basic_handwashing_facilities,
                    i.safely_managed_drinking_water_services,
                    i.access_to_electricity,
                    i.energy_use,
                    i.alternative_and_nuclear_energy,
                    i.permanent_cropland,
                    i.crop_production_index,
                    i.gdp_per_unit_of_energy_use
                FROM (
                    SELECT
                        COALESCE(ei.provider_id, hi.provider_id, env.provider_id) AS provider_id,
                        COALESCE(ei.economy_code, hi.economy_code, env.economy_code) AS economy_code,
                        COALESCE(ei.year, hi.year, env.year) AS year,

                        ei.gdp_per_capita,
                        ei.industry,
                        ei.trade,
                        ei.agriculture_forestry_and_fishing,

                        hi.community_health_workers,
                        hi.diabetes_prevalence,
                        hi.prevalence_of_undernourishment,
                        hi.prevalence_of_severe_food_insecurity,
                        hi.basic_handwashing_facilities,
                        hi.safely_managed_drinking_water_services,

                        env.access_to_electricity,
                        env.energy_use,
                        env.alternative_and_nuclear_energy,
                        env.permanent_cropland,
                        env.crop_production_index,
                        env.gdp_per_unit_of_energy_use
                    FROM economic_indicators ei
                    FULL OUTER JOIN health_indicators hi
                        USING (provider_id, economy_code, year)
                    FULL OUTER JOIN environment_indicators env
                        USING (provider_id, economy_code, year)
                ) i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                LEFT JOIN income_levels il ON e.income_level = il.id
                {where_clause}
                ORDER BY i.year DESC, e.name
                LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """, *params)
            return [dict(row) for row in rows]

    async def list_economic_indicators(
        self, filters: IndicatorFilters
    ) -> List[dict]:
        """List economic indicators only with filters."""
        extra = [
            "(i.gdp_per_capita IS NOT NULL OR i.industry IS NOT NULL "
            "OR i.trade IS NOT NULL)"
        ]
        where_clause, params, param_idx = build_indicator_filter_clause(
            filters, extra)
        params.extend([filters.limit, filters.offset])

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT
                    e.code AS economy_code,
                    e.name AS economy_name,
                    r.name AS region_name,
                    i.year,
                    i.gdp_per_capita,
                    i.industry,
                    i.trade,
                    i.agriculture_forestry_and_fishing,
                    p.name AS provider_name
                FROM economic_indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                {where_clause}
                ORDER BY i.year DESC, e.name
                LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """, *params)
            return [dict(row) for row in rows]

    async def list_health_indicators(
        self, filters: IndicatorFilters
    ) -> List[dict]:
        """List health indicators only with filters."""
        extra = [
            "(i.community_health_workers IS NOT NULL "
            "OR i.diabetes_prevalence IS NOT NULL "
            "OR i.prevalence_of_undernourishment IS NOT NULL)"
        ]
        where_clause, params, param_idx = build_indicator_filter_clause(
            filters, extra)
        params.extend([filters.limit, filters.offset])

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT
                    e.code AS economy_code,
                    e.name AS economy_name,
                    r.name AS region_name,
                    i.year,
                    i.community_health_workers,
                    i.diabetes_prevalence,
                    i.prevalence_of_undernourishment,
                    i.prevalence_of_severe_food_insecurity,
                    i.basic_handwashing_facilities,
                    i.safely_managed_drinking_water_services,
                    p.name AS provider_name
                FROM health_indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                {where_clause}
                ORDER BY i.year DESC, e.name
                LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """, *params)
            return [dict(row) for row in rows]

    async def list_environment_indicators(
        self, filters: IndicatorFilters
    ) -> List[dict]:
        """List environment indicators only with filters."""
        extra = [
            "(i.access_to_electricity IS NOT NULL "
            "OR i.energy_use IS NOT NULL "
            "OR i.alternative_and_nuclear_energy IS NOT NULL)"
        ]
        where_clause, params, param_idx = build_indicator_filter_clause(
            filters, extra)
        params.extend([filters.limit, filters.offset])

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT
                    e.code AS economy_code,
                    e.name AS economy_name,
                    r.name AS region_name,
                    i.year,
                    i.access_to_electricity,
                    i.energy_use,
                    i.alternative_and_nuclear_energy,
                    i.permanent_cropland,
                    i.crop_production_index,
                    i.gdp_per_unit_of_energy_use,
                    p.name AS provider_name
                FROM environment_indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                {where_clause}
                ORDER BY i.year DESC, e.name
                LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """, *params)
            return [dict(row) for row in rows]

    async def get_stats(self) -> dict:
        """Get database statistics."""
        async with self.pool.acquire() as conn:
            stats = {}
            stats['economies'] = await conn.fetchval(
                "SELECT COUNT(*) FROM economies")
            stats['providers'] = await conn.fetchval(
                "SELECT COUNT(*) FROM providers WHERE immutable = false")
            stats['indicators'] = await conn.fetchval(
                "SELECT COUNT(*) FROM indicators")
            year_row = await conn.fetchrow(
                "SELECT MIN(year) as min_year, MAX(year) as max_year "
                "FROM indicators"
            )
            stats['year_range'] = dict(year_row) if year_row else {
                'min_year': None, 'max_year': None
            }
            return stats
