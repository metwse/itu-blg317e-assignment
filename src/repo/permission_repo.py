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
