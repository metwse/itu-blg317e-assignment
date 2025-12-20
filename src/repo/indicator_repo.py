from . import BaseRepo

from src.dto import IndicatorCreateDto, IndicatorUpdateDto
from src.entities import Indicator


class IndicatorRepo(BaseRepo[Indicator, IndicatorUpdateDto, IndicatorCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'indicators',
                         ['provider_id', 'economy_code', 'year'],
                         (Indicator, IndicatorUpdateDto, IndicatorCreateDto))
