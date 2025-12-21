"""Public service layer for read-only data access."""

from typing import List

from src.repo.public_repo import PublicRepo
from src.handlers.util import IndicatorFilters


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

    async def list_indicators(self, filters: IndicatorFilters) -> List[dict]:
        """List all indicators with filters."""
        return await self.repo.list_indicators(filters)

    async def list_economic_indicators(
        self, filters: IndicatorFilters
    ) -> List[dict]:
        """List economic indicators with filters."""
        return await self.repo.list_economic_indicators(filters)

    async def list_health_indicators(
        self, filters: IndicatorFilters
    ) -> List[dict]:
        """List health indicators with filters."""
        return await self.repo.list_health_indicators(filters)

    async def list_environment_indicators(
        self, filters: IndicatorFilters
    ) -> List[dict]:
        """List environment indicators with filters."""
        return await self.repo.list_environment_indicators(filters)

    async def get_stats(self) -> dict:
        """Get database statistics."""
        return await self.repo.get_stats()
