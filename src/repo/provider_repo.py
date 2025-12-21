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

    async def get_providers_by_user(self, user_id: int):
        """Fetch all providers where the user is admin or technical account.

        Args:
            user_id: The user's ID.

        Returns:
            List of providers with id, name, and role ('admin' or 'technical').
        """
        return await self.fetch_raw(
            """
            SELECT
                id,
                name,
                immutable,
                CASE
                    WHEN administrative_account = $1 THEN 'admin'
                    WHEN technical_account = $1 THEN 'technical'
                END AS role
            FROM providers
            WHERE administrative_account = $1 OR technical_account = $1
            ORDER BY name
            """,
            user_id
        )

    async def get_provider_by_id(self, provider_id: int):
        """Fetch a single provider by ID.

        Args:
            provider_id: The provider's ID.

        Returns:
            The provider record if found.
        """
        return await self.fetchrow_raw(
            """
            SELECT * FROM providers WHERE id = $1
            """,
            provider_id
        )

    async def validate_user_provider_access(self, user_id: int,
                                            provider_id: int):
        """Check if a user has access to a specific provider.

        Args:
            user_id: The user's ID.
            provider_id: The provider's ID.

        Returns:
            Dict with provider info and role if access is granted, None
            otherwise.
        """
        return await self.fetchrow_raw(
            """
            SELECT
                id,
                name,
                immutable,
                CASE
                    WHEN administrative_account = $1 THEN 'admin'
                    WHEN technical_account = $1 THEN 'technical'
                END AS role
            FROM providers
            WHERE id = $2
              AND (administrative_account = $1 OR technical_account = $1)
            """,
            user_id, provider_id
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
