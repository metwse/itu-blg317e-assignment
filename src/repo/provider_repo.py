from . import BaseRepo

from src.dto import ProviderCreateDto, ProviderUpdateDto
from src.entities import Provider


class ProviderRepo(BaseRepo[Provider, ProviderUpdateDto, ProviderCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'providers', ['id'],
                         (Provider, ProviderUpdateDto, ProviderCreateDto))
