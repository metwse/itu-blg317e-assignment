"""World Bank economic development indicators data loader."""

from fixtures.worldbank_api import \
    HEALTH_INDICATORS, ECONOMIC_INDICATORS, ENVIRONMENT_INDICATORS, \
    fetch_indicators

from src import log
from src.service.base_service import BaseService
from src.state import State
from src.entities import \
    HealthIndicator, EconomicIndicator, EnvironmentIndicator

from typing import TypeVar
from pydantic import BaseModel
import asyncio

T = TypeVar('T', bound=BaseModel)


def to_rows(ModelClass: type[BaseModel], data, economy):
    rows = []
    cardinality = len(data[list(ModelClass.model_fields.keys())[-1]])

    for i in range(cardinality):
        row = {'provider_id': 1, 'economy_code': economy}

        for field_name in ModelClass.model_fields:
            if field_name in data:
                row['year'] = data[field_name][i][0]
                row[field_name] = data[field_name][i][1]

        rows.append(ModelClass(**row))

    return rows


async def insert_rows(service: BaseService, rows: list[BaseModel]):
    await asyncio.gather(*map(lambda row: service.create(row), rows))


async def load(state: State, last_step, set_last_step):
    economies = [*map(lambda economy: economy.code,
                      await state.economy_service.list(99999999, 0))]

    i = 0 if last_step is None else economies.index(last_step) + 1

    for economy in economies[i:]:
        log.info(f"Fetching health indicators for {economy}...")
        health_indicators = \
            await fetch_indicators(HEALTH_INDICATORS, economy)

        log.info(f"Fetching economic indicators for {economy}...")
        economic_indicators = \
            await fetch_indicators(ECONOMIC_INDICATORS, economy)

        log.info(f"Fetching environment indicators for {economy}...")
        environment_indicator = \
            await fetch_indicators(ENVIRONMENT_INDICATORS, economy)

        log.info(f"Inserting indicators for {economy} to database...")
        await asyncio.gather(
            insert_rows(state.health_indicator_service,
                        to_rows(HealthIndicator, health_indicators,
                                economy)),
            insert_rows(state.economic_indicator_service,
                        to_rows(EconomicIndicator, economic_indicators,
                                economy)),
            insert_rows(state.environment_indicator_service,
                        to_rows(EnvironmentIndicator, environment_indicator,
                                economy))
        )

        set_last_step(economy)
        i += 1
