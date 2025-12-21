"""Public API routes for viewing data (no authentication required)."""

from flask import Blueprint, jsonify, request
import asyncpg


def public_routes(pool: asyncpg.pool.Pool):
    """Create public API routes for viewing indicator data with joins.

    Args:
        pool: Database connection pool.

    Returns:
        Flask Blueprint with public data routes.
    """
    public = Blueprint("public", __name__, url_prefix="/api/public")

    @public.route("/economies", methods=["GET"])
    async def list_economies():
        """List all economies with region and income level names."""
        async with pool.acquire() as conn:
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
            return jsonify([dict(row) for row in rows])

    @public.route("/regions", methods=["GET"])
    async def list_regions():
        """List all regions."""
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM regions ORDER BY name")
            return jsonify([dict(row) for row in rows])

    @public.route("/income-levels", methods=["GET"])
    async def list_income_levels():
        """List all income levels."""
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM income_levels ORDER BY name")
            return jsonify([dict(row) for row in rows])

    @public.route("/providers", methods=["GET"])
    async def list_providers():
        """List all providers with admin/tech user names."""
        async with pool.acquire() as conn:
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
            return jsonify([dict(row) for row in rows])

    @public.route("/indicators", methods=["GET"])
    async def list_indicators():
        """List indicators with economy and provider info.

        Query params:
            - economy_code: Filter by economy code
            - region: Filter by region code
            - year: Filter by specific year
            - year_start: Filter by year range start
            - year_end: Filter by year range end
            - provider_id: Filter by provider
            - limit: Max results (default 100)
            - offset: Pagination offset
        """
        economy_code = request.args.get('economy_code')
        region = request.args.get('region')
        year = request.args.get('year')
        year_start = request.args.get('year_start')
        year_end = request.args.get('year_end')
        provider_id = request.args.get('provider_id')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        conditions = []
        params = []
        param_idx = 1

        if economy_code:
            conditions.append(f"i.economy_code = ${param_idx}")
            params.append(economy_code.upper())
            param_idx += 1

        if region:
            conditions.append(f"e.region = ${param_idx}")
            params.append(region.upper())
            param_idx += 1

        if year:
            conditions.append(f"i.year = ${param_idx}")
            params.append(int(year))
            param_idx += 1
        else:
            if year_start:
                conditions.append(f"i.year >= ${param_idx}")
                params.append(int(year_start))
                param_idx += 1
            if year_end:
                conditions.append(f"i.year <= ${param_idx}")
                params.append(int(year_end))
                param_idx += 1

        if provider_id:
            conditions.append(f"i.provider_id = ${param_idx}")
            params.append(int(provider_id))
            param_idx += 1

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        params.extend([limit, offset])

        async with pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT 
                    i.provider_id,
                    p.name AS provider_name,
                    i.economy_code,
                    e.name AS economy_name,
                    r.name AS region_name,
                    il.name AS income_level,
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
                FROM indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                LEFT JOIN income_levels il ON e.income_level = il.id
                {where_clause}
                ORDER BY i.year DESC, e.name
                LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """, *params)
            return jsonify([dict(row) for row in rows])

    @public.route("/indicators/economic", methods=["GET"])
    async def list_economic_indicators():
        """List economic indicators only."""
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        async with pool.acquire() as conn:
            rows = await conn.fetch("""
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
                FROM indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                WHERE i.gdp_per_capita IS NOT NULL 
                   OR i.industry IS NOT NULL
                   OR i.trade IS NOT NULL
                ORDER BY i.year DESC, e.name
                LIMIT $1 OFFSET $2
            """, limit, offset)
            return jsonify([dict(row) for row in rows])

    @public.route("/indicators/health", methods=["GET"])
    async def list_health_indicators():
        """List health indicators only."""
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        async with pool.acquire() as conn:
            rows = await conn.fetch("""
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
                FROM indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                WHERE i.community_health_workers IS NOT NULL
                   OR i.diabetes_prevalence IS NOT NULL
                   OR i.prevalence_of_undernourishment IS NOT NULL
                ORDER BY i.year DESC, e.name
                LIMIT $1 OFFSET $2
            """, limit, offset)
            return jsonify([dict(row) for row in rows])

    @public.route("/indicators/environment", methods=["GET"])
    async def list_environment_indicators():
        """List environment indicators only."""
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        async with pool.acquire() as conn:
            rows = await conn.fetch("""
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
                FROM indicators i
                JOIN economies e ON i.economy_code = e.code
                JOIN providers p ON i.provider_id = p.id
                LEFT JOIN regions r ON e.region = r.id
                WHERE i.access_to_electricity IS NOT NULL
                   OR i.energy_use IS NOT NULL
                   OR i.alternative_and_nuclear_energy IS NOT NULL
                ORDER BY i.year DESC, e.name
                LIMIT $1 OFFSET $2
            """, limit, offset)
            return jsonify([dict(row) for row in rows])

    @public.route("/stats", methods=["GET"])
    async def get_stats():
        """Get database statistics."""
        async with pool.acquire() as conn:
            stats = {}
            stats['economies'] = await conn.fetchval(
                "SELECT COUNT(*) FROM economies")
            stats['providers'] = await conn.fetchval(
                "SELECT COUNT(*) FROM providers WHERE immutable = false")
            stats['indicators'] = await conn.fetchval(
                "SELECT COUNT(*) FROM indicators")
            stats['year_range'] = dict(await conn.fetchrow(
                "SELECT MIN(year) as min_year, MAX(year) as max_year FROM indicators"
            ) or {'min_year': None, 'max_year': None})
            return jsonify(stats)

    return public
