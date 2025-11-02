from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CountryState:
    code: str
    data: Dict[str, Any]
