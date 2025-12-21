from . import BaseRepo

from src.dto import PermissionCreateDto, PermissionUpdateDto
from src.entities import Permission


class PermissionRepo(BaseRepo[Permission, PermissionUpdateDto,
                     PermissionCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'permissions', ['id'],
                         (Permission, PermissionUpdateDto,
                          PermissionCreateDto))

    async def get_permissions_by_provider(self, provider_id):  # MANAGEMENT
        return await self.fetch_raw(
            """
            SELECT * FROM permissions
            WHERE provider_id = $1
            ORDER BY year_start DESC, id DESC
            """,
            provider_id
        )

    async def get_permissions_for_portal(self, provider_id: int):
        """Fetch permissions for portal display with simplified scope info.

        Args:
            provider_id: The provider's ID.

        Returns:
            List of permissions with scope, type, and year range.
        """
        return await self.fetch_raw(
            """
            SELECT
                id,
                COALESCE(economy_code, region) AS scope,
                CASE
                    WHEN economy_code IS NOT NULL THEN 'economy'
                    ELSE 'region'
                END AS type,
                year_start,
                year_end
            FROM permissions
            WHERE provider_id = $1
            ORDER BY year_start DESC, id DESC
            """,
            provider_id
        )

    async def check_permission_for_economy(self, provider_id: int,
                                           economy_code: str, year: int):
        """Check if a provider has permission to write data for an economy/year.

        Checks both direct economy permissions and region-based permissions.

        Args:
            provider_id: The provider's ID.
            economy_code: The economy code (e.g., 'TUR').
            year: The year for data entry.

        Returns:
            The matching permission record if found, None otherwise.
        """
        return await self.fetchrow_raw(
            """
            SELECT p.id, p.provider_id, p.economy_code, p.region,
                   p.year_start, p.year_end
            FROM permissions p
            LEFT JOIN economies e ON e.code = $2
            WHERE p.provider_id = $1
              AND $3 BETWEEN p.year_start AND p.year_end
              AND (
                  p.economy_code = $2
                  OR p.region = e.region
              )
            LIMIT 1
            """,
            provider_id, economy_code, year
        )

    async def create_permission(self, provider_id, year_start, year_end,
                                economy_code, region, footnote):  # MANAGEMENT
        return await self.fetchrow_raw(
            """
            INSERT INTO permissions
                (provider_id, year_start, year_end,
                 economy_code, region, footnote)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """,
            provider_id, year_start, year_end, economy_code, region, footnote
        )

    async def delete_permission(self, id: int):  # MANAGEMENT
        return await self.fetchrow_raw(
            """
            DELETE FROM permissions WHERE id = $1
            RETURNING id
            """,
            id
        )
