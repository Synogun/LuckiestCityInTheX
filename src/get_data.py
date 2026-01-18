import json
from time import sleep
from typing import Any

import requests

from data_handler import read_json_file

API_KEY = "YOUR_API_KEY"


def save_response_to_file(data: Any, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        if filename.endswith(".json"):
            import json

            json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            file.write(data)


def get_country_details(country_iso2: str, country_name: str) -> dict[str, Any] | None:
    response = requests.get(
        f"https://api.countrystatecity.in/v1/countries/{country_iso2}",
        headers={"X-CSCAPI-KEY": API_KEY},
    )

    if response.ok:
        data: dict[str, Any] = response.json()
        print(
            f"Found details for country code: {data['name']} ({data['iso2']}) {data['emoji']}"
        )
        return data
    else:
        print(f"{country_name} ({country_iso2}) details not found.")
        return None


def process_country_details():
    countries: list[dict[str, str]] = []
    with open("data/world_countries.json", "r", encoding="utf-8") as file:
        countries = json.load(file)

    country_details: dict[str, dict[str, Any] | None] = {}
    for country in countries:
        country_iso2 = country["iso2"]
        country_name = country["name"]

        sleep(1)  # To avoid hitting API rate limits

        country = get_country_details(country_iso2, country_name)
        country_details[country_iso2] = country

        save_response_to_file(country_details, "data/world_countries_details.json")


def main() -> None:

    _cities_data = read_json_file("data/world_cities.json")
    _states_data = read_json_file("data/world_states.json")
    countries_data = read_json_file("data/world_countries.json")
    country_details_data = read_json_file("data/world_countries_details.json")

    country_map = {c["iso2"]: c for c in countries_data}
    country_details_map = {c["iso2"]: c for c in country_details_data.values()}

    country_map = {
        c["iso2"]: {**c, **country_details_map.get(c["iso2"], {})}
        for c in country_map.values()
    }

    with open("data/full_world_countries.json", "w", encoding="utf-8") as file:
        json.dump(list(country_map.values()), file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
