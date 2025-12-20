from . import BaseRepo

from src.dto import ProviderCreateDto, ProviderUpdateDto
from src.entities import Provider


class ProviderRepo(BaseRepo[Provider, ProviderUpdateDto, ProviderCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'providers', ['id'],
                         (Provider, ProviderUpdateDto, ProviderCreateDto))

    async def get_all_providers(self):
        return await self.fetch_raw(
            "SELECT * FROM providers"
        )

    async def create_provider(self,
                              administrative_account, technical_account,
                              name, description, website_url, immutable):
        return await self.fetchrow_raw(
            """
            INSERT INTO providers
                (administrative_account, technical_account,
                 name, description, website_url, immutable)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """,
            administrative_account, technical_account,
            name, description, website_url, immutable
        )

    async def delete_provider(self, id):
        return await self.fetchrow_raw(
            """
            DELETE FROM providers WHERE id = $1
            RETURNING id
            """,
            id
        )
