"""Public handler for read-only data access."""

from flask import jsonify

from src.service.public_service import PublicService
from .util import parse_indicator_filters


class PublicHandler:
    """Handler for public API endpoints.

    This handler provides HTTP interface for public data access,
    delegating all business logic to the service layer.
    """

    def __init__(self, service: PublicService):
        self.service = service

    async def list_economies(self):
        """List all economies with region and income level."""
        data = await self.service.list_economies()
        return jsonify(data)

    async def list_regions(self):
        """List all regions."""
        data = await self.service.list_regions()
        return jsonify(data)

    async def list_income_levels(self):
        """List all income levels."""
        data = await self.service.list_income_levels()
        return jsonify(data)

    async def list_providers(self):
        """List all providers with user names."""
        data = await self.service.list_providers()
        return jsonify(data)

    async def list_indicators(self):
        """List all indicators with filters from query params."""
        filters = parse_indicator_filters()
        data = await self.service.list_indicators(filters)
        return jsonify(data)

    async def list_economic_indicators(self):
        """List economic indicators with filters."""
        filters = parse_indicator_filters()
        data = await self.service.list_economic_indicators(filters)
        return jsonify(data)

    async def list_health_indicators(self):
        """List health indicators with filters."""
        filters = parse_indicator_filters()
        data = await self.service.list_health_indicators(filters)
        return jsonify(data)

    async def list_environment_indicators(self):
        """List environment indicators with filters."""
        filters = parse_indicator_filters()
        data = await self.service.list_environment_indicators(filters)
        return jsonify(data)

    async def get_stats(self):
        """Get database statistics."""
        data = await self.service.get_stats()
        return jsonify(data)
