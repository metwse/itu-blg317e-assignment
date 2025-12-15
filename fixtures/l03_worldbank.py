"""World Bank economic development indicators data loader."""

from fixtures.worldbank_api import HEALTH_INDICATORS, fetch_indicators
from src.state import State


async def load(state: State):
    economies = [*map(lambda economy: economy.code,
                      await state.economy_service.list(99999999, 0))]

    print(await fetch_indicators(HEALTH_INDICATORS, economies))
