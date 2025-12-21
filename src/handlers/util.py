from src.error import AppError, AppErrorType

from flask import request
from dataclasses import dataclass
from typing import Optional


def json():
    json = request.get_json()

    if not json:
        raise AppError(AppErrorType.JSON_PARSE_ERROR,
                       "could not serialize json")

    return json


@dataclass
class IndicatorFilters:
    """Common filters for indicator queries."""
    economy_code: Optional[str] = None
    region: Optional[str] = None
    year: Optional[int] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    provider_id: Optional[int] = None
    limit: int = 100
    offset: int = 0


def parse_indicator_filters() -> IndicatorFilters:
    """Parse indicator filter parameters from request query string."""
    economy_code = request.args.get('economy_code')
    region = request.args.get('region')
    year = request.args.get('year')
    year_start = request.args.get('year_start')
    year_end = request.args.get('year_end')
    provider_id = request.args.get('provider_id')
    limit = request.args.get('limit', '100')
    offset = request.args.get('offset', '0')

    return IndicatorFilters(
        economy_code=economy_code,
        region=region,
        year=int(year) if year else None,
        year_start=int(year_start) if year_start else None,
        year_end=int(year_end) if year_end else None,
        provider_id=int(provider_id) if provider_id else None,
        limit=int(limit),
        offset=int(offset)
    )
