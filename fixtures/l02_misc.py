"""Miscellaneous initial data."""

from src.dto import ProviderCreateDto
from src.state import State


async def load(state: State, *_):
    await state.provider_service.create(
        ProviderCreateDto(email="worldbank@example.com",
                          name="World Bank",
                          password_hash="nologin",
                          nologin=True,
                          is_admin=False))
