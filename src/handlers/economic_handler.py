from flask import request, jsonify
from src.entities import EconomicIndicator
from src.service.economic_service import EconomicService

class EconomicHandler:
    def __init__(self, service: EconomicService, loop):
        self._service = service
        self._loop = loop

    def list_indicators(self, code: str):
        provider_id = int(request.headers.get("X-Provider-Id", 1))
        indicators = self._loop.run_until_complete(
            self._service.list_indicators(provider_id, code)
        )
        return jsonify([i.__dict__ for i in indicators])

    def create_indicator(self):
        data = request.get_json()
        indicator = EconomicIndicator(**data)
        result = self._loop.run_until_complete(
            self._service.create_indicator(indicator)
        )
        return jsonify({"result": result}), 201
