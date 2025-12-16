"""World Bank economic development indicators data loader."""

from fixtures.worldbank_api import \
    HEALTH_INDICATORS, ECONOMIC_INDICATORS, ENVIRONMENT_INDICATORS, \
    fetch_indicators
from src.state import State


async def load(state: State, last_step, set_last_step):
    economies = [*map(lambda economy: economy.code,
                      await state.economy_service.list(99999999, 0))]

    print(last_step)
    i = 0 if last_step is None else economies.index(last_step)

    for economy in economies[i:]:
        await fetch_indicators(HEALTH_INDICATORS, economy)
        await fetch_indicators(ECONOMIC_INDICATORS, economy)
        await fetch_indicators(ENVIRONMENT_INDICATORS, economy)
        set_last_step(economy)
        i += 1
