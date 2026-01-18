import json
from typing import Any

from data_types import CityTypeData, CountryTypeData

from .simulation import SimulationResult


def read_json_file(filename: str) -> Any:
    """Reads a JSON file and returns its content."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results_to_file(
    analysis: str,
    results: SimulationResult,
    filename: str,
) -> None:
    """Saves the analysis and results to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(analysis + "\n\n")

        for index, day_result in enumerate(results, start=1):
            file.write(
                f"{index}º {day_result[1]} on {day_result[0].strftime('%d-%m-%Y')}\n"
            )


def get_country_code(
    countries_data: CountryTypeData,
    country_name: str,
) -> str | None:
    """Gets the country code for a given country name."""
    for country in countries_data:
        country_name_data = country.get("name")
        if country_name_data and country_name_data.lower() == country_name.lower():
            return country.get("iso2")
    return None
