"""Public service layer for read-only data access."""

from typing import List, Optional

from src.repo.public_repo import PublicRepo


class PublicService:
    """Service layer for public API.
    
    This service provides read-only access to joined indicator data.
    It acts as a thin wrapper around PublicRepo, following the SoC principle.
    """

    def __init__(self, pool):
        self.repo = PublicRepo(pool)

    async def list_economies(self) -> List[dict]:
        """List all economies with region and income level."""
        return await self.repo.list_economies()

    async def list_regions(self) -> List[dict]:
        """List all regions."""
        return await self.repo.list_regions()

    async def list_income_levels(self) -> List[dict]:
        """List all income levels."""
        return await self.repo.list_income_levels()

    async def list_providers(self) -> List[dict]:
        """List all providers with user names."""
        return await self.repo.list_providers()

    async def list_indicators(
        self,
        economy_code: Optional[str] = None,
        region: Optional[str] = None,
        year: Optional[int] = None,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        provider_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """List indicators with filters."""
        return await self.repo.list_indicators(
            economy_code=economy_code,
            region=region,
            year=year,
            year_start=year_start,
            year_end=year_end,
            provider_id=provider_id,
            limit=limit,
            offset=offset
        )

    async def list_economic_indicators(
        self, limit: int = 100, offset: int = 0
    ) -> List[dict]:
        """List economic indicators."""
        return await self.repo.list_economic_indicators(limit, offset)

    async def list_health_indicators(
        self, limit: int = 100, offset: int = 0
    ) -> List[dict]:
        """List health indicators."""
        return await self.repo.list_health_indicators(limit, offset)

    async def list_environment_indicators(
        self, limit: int = 100, offset: int = 0
    ) -> List[dict]:
        """List environment indicators."""
        return await self.repo.list_environment_indicators(limit, offset)

    async def get_stats(self) -> dict:
        """Get database statistics."""
        return await self.repo.get_stats()
