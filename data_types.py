from datetime import date
from typing import Any

type CityTypeData = dict[str, list[dict[str, str | None]]]
type CountryTypeData = list[dict[str, Any]]
type SimulationResult = list[tuple[date, dict[str, Any]]]

__all__ = [
    "CityTypeData",
    "CountryTypeData",
    "SimulationResult",
]
