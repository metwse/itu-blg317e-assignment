from . import BaseRepo

from src.dto import EconomyCreateDto, EconomyUpdateDto
from src.entities import Economy


class EconomyRepo(BaseRepo[Economy, EconomyUpdateDto, EconomyCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'economies', ['code'],
                         (Economy, EconomyUpdateDto, EconomyCreateDto))
