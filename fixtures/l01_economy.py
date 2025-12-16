"""Load economies table (names, codes, regions)."""

from fixtures.worldbank_api import REGION_MAPPING, fetch

from src.entities import Economy, Region
from src.state import State

from typing import cast


async def load(state: State, *_):
    economies = await fetch("country", all=True)

    for economy in economies:
        region = REGION_MAPPING[economy['region']['id']] \
            if economy['region']['id'] != 'NA' else None

        await state.economy_service.create(
            Economy(code=cast(str, economy['id']),
                    name=cast(str, economy['name']),
                    region=cast(Region | None, region)))
