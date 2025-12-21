"""Public handler for read-only data access."""

from flask import jsonify, request

from src.service.public_service import PublicService


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
        """List indicators with filters from query params."""
        economy_code = request.args.get('economy_code')
        region = request.args.get('region')
        year = request.args.get('year')
        year_start = request.args.get('year_start')
        year_end = request.args.get('year_end')
        provider_id = request.args.get('provider_id')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        data = await self.service.list_indicators(
            economy_code=economy_code,
            region=region,
            year=int(year) if year else None,
            year_start=int(year_start) if year_start else None,
            year_end=int(year_end) if year_end else None,
            provider_id=int(provider_id) if provider_id else None,
            limit=limit,
            offset=offset
        )
        return jsonify(data)

    async def list_economic_indicators(self):
        """List economic indicators."""
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        data = await self.service.list_economic_indicators(limit, offset)
        return jsonify(data)

    async def list_health_indicators(self):
        """List health indicators."""
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        data = await self.service.list_health_indicators(limit, offset)
        return jsonify(data)

    async def list_environment_indicators(self):
        """List environment indicators."""
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        data = await self.service.list_environment_indicators(limit, offset)
        return jsonify(data)

    async def get_stats(self):
        """Get database statistics."""
        data = await self.service.get_stats()
        return jsonify(data)
