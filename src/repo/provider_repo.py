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

    async def get_provider_details_for_portal(self, provider_id: int):
        """Get provider details including technical account info for portal.

        Args:
            provider_id: The provider's ID.

        Returns:
            Provider details with technical account user info.
        """
        return await self.fetchrow_raw(
            """
            SELECT
                p.id,
                p.name,
                p.description,
                p.website_url,
                p.technical_account,
                u.name AS technical_account_name,
                u.email AS technical_account_email
            FROM providers p
            LEFT JOIN users u ON p.technical_account = u.id
            WHERE p.id = $1
            """,
            provider_id
        )

    async def update_provider_from_portal(self, provider_id: int,
                                          technical_account,
                                          clear_technical_account: bool,
                                          description: str | None,
                                          clear_description: bool,
                                          website_url: str | None,
                                          clear_website_url: bool):
        """Update provider details from portal (admin only).

        Args:
            provider_id: The provider's ID.
            technical_account: New technical account user ID.
            clear_technical_account: If True, set technical_account to NULL.
            description: New description (or None to keep existing).
            clear_description: If True, set description to NULL.
            website_url: New website URL (or None to keep existing).
            clear_website_url: If True, set website_url to NULL.

        Returns:
            Updated provider record.
        """
        # Build dynamic update based on what's provided
        set_parts = []
        params = [provider_id]
        param_idx = 2

        if clear_technical_account:
            set_parts.append("technical_account = NULL")
        elif technical_account is not None:
            set_parts.append(f"technical_account = ${param_idx}")
            params.append(technical_account)
            param_idx += 1

        if clear_description:
            set_parts.append("description = NULL")
        elif description is not None:
            set_parts.append(f"description = ${param_idx}")
            params.append(description)
            param_idx += 1

        if clear_website_url:
            set_parts.append("website_url = NULL")
        elif website_url is not None:
            set_parts.append(f"website_url = ${param_idx}")
            params.append(website_url)
            param_idx += 1

        if not set_parts:
            # Nothing to update, just return current
            return await self.get_provider_by_id(provider_id)

        query = f"""
            UPDATE providers
            SET {', '.join(set_parts)}
            WHERE id = $1
            RETURNING id, name, description, website_url, technical_account
        """

        return await self.fetchrow_raw(query, *params)
