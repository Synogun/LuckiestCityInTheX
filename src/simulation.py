from datetime import date, datetime, timedelta
from random import randint
from typing import Any, Callable

from data_types import CityTypeData, CountryTypeData, SimulationResult
from src.analysis import analyze_pool_results
from src.data_handler import get_country_code, read_json_file, save_results_to_file


def run_simulation(
    starting_date: date | None = None,
    draw_pool: list[dict[str, str]] = [],
) -> SimulationResult:
    """
    Runs the elimination simulation for a draw pool.

    Returns a list of results in winning order, where each result is a tuple:
    (elimination_date: date, draw_info: dict[str, Any])
    """

    current_day: date = starting_date or date.today()
    results: SimulationResult = []
    pool_list = draw_pool.copy()

    while len(pool_list) > 0:
        random_number = randint(0, len(pool_list) - 1)

        draw = pool_list.pop(random_number)

        results.append((current_day, draw))

        current_day += timedelta(days=1)
    results.reverse()

    return results


def country_city_royale(
    starting_date: date | None = None,
    country_name: str | None = None,
    my_city_name: str | None = None,
    save_to_file: bool = False,
    print_to_console: bool = True,
) -> tuple[dict[str, Any], SimulationResult, list[str]]:
    """Executes a city royale simulation for a specific country and returns the results."""

    def final_print(logs: list[str]) -> None:
        if print_to_console:
            print("\n".join(logs))

    console_logs: list[str] = []
    default_return: Callable[[], tuple[dict[str, Any], SimulationResult, list[str]]] = (
        lambda: ({}, [], [])
    )

    console_logs.append("--- Country City Royale ---\n")
    console_logs.append("There can only be one LUCKIEST CITY IN THE COUNTRY!\n")

    # --- Configuration ---
    COUNTRY_NAME = country_name or "Canada"
    MY_CITY = my_city_name or "Vancouver"
    # --- End of Configuration ---

    # Load data
    countries_data: CountryTypeData = read_json_file("data/full_world_countries.json")
    cities_data: CityTypeData = read_json_file("data/world_cities.json")

    # Get country code
    country_code = get_country_code(countries_data, COUNTRY_NAME)

    if not country_code:
        console_logs.append(f"Country '{COUNTRY_NAME}' not found.")
        final_print(console_logs)

        return default_return()
    else:
        console_logs.append(f"Country Code: {country_code}")

    # Get cities for the selected country
    country_cities: list[dict[str, Any]] = cities_data.get(country_code, [])

    if not country_cities:
        console_logs.append(f"No cities found for {COUNTRY_NAME}.\n")
        final_print(console_logs)

        return default_return()
    else:
        console_logs.append(
            f"Number of cities found for {COUNTRY_NAME}: {len(country_cities)}\n"
        )

    # Run simulation
    results: SimulationResult = run_simulation(
        starting_date=starting_date,
        draw_pool=country_cities,
    )

    # Analyze results
    country_result, analysis = analyze_pool_results(
        results,
        COUNTRY_NAME,
        MY_CITY,
    )
    console_logs.append(analysis)

    # Save results
    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        formated_cname = COUNTRY_NAME.lower().replace(" ", "_")

        save_results_to_file(
            analysis,
            results,
            f"logs/{formated_cname}-city-royale-{timestamp}.txt",
        )

    final_print(console_logs)
    return country_result, results, console_logs


def global_city_royale(
    starting_date: date = date.today(),
    tracked_city_name: str | None = None,
    save_to_file: bool = False,
    print_to_console: bool = True,
    draw_simultaneous_countries: bool = True,
) -> tuple[dict[str, Any], SimulationResult, list[str]]:
    """Executes a city royale simulation for the whole world and returns the results."""

    def final_print(logs: list[str]) -> None:
        if print_to_console:
            print("\n".join(logs))

    if not starting_date:
        starting_date = date.today()

    console_logs: list[str] = []

    console_logs.append("--- Global City Royale ---\n")
    console_logs.append("There can only be one LUCKIEST CITY IN THE WORLD!\n")

    # --- Configuration ---
    TRACKED_CITY = tracked_city_name or "Vancouver"
    # --- End of Configuration ---

    # Load data
    countries_data: CountryTypeData = read_json_file("data/full_world_countries.json")
    cities_data: CityTypeData = read_json_file("data/world_cities.json")

    global_pool: list[dict[str, Any]] = []

    console_logs.append("Running country-level simulations...\n")

    longest_simulation: int = 0
    for country in countries_data:
        country_cities: list[dict[str, Any]] = cities_data.get(
            str(country.get("iso2")),
            [],
        )

        if not country_cities:
            console_logs.append(f"Country: {country.get('name')} | Cities: 0")
            continue

        if not draw_simultaneous_countries:
            global_pool.extend(country_cities)

            console_logs.append(
                f"Country: {country.get('name')} | Cities: {len(country_cities)}"
            )
            continue

        simulation_result: SimulationResult = run_simulation(
            starting_date=starting_date,
            draw_pool=country_cities,
        )
        country_winner = simulation_result[0][1]
        global_pool.append(country_winner)

        if len(simulation_result) > longest_simulation:
            longest_simulation = len(simulation_result)
            console_logs.append(
                f"Country: {country.get('name')} | Cities: {len(country_cities)} (Longest so far!)"
            )
        else:
            console_logs.append(
                f"Country: {country.get('name')} | Cities: {len(country_cities)}"
            )

        # If each country starts drawing on the same day,
        # we need to wait for the longest simulation to end
        # If not, we can proceed to the global simulation right away
        # as all the cities will be eliminated one by one
    if draw_simultaneous_countries:
        starting_date = starting_date + timedelta(days=longest_simulation)

    # Run simulation
    results: SimulationResult = run_simulation(
        starting_date=starting_date,
        draw_pool=global_pool,
    )

    # Analyze results
    world_result, analysis = analyze_pool_results(
        results,
        "World",
        TRACKED_CITY,
    )
    console_logs.append(analysis)

    # Save results
    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        save_results_to_file(
            analysis,
            results,
            f"logs/global-city-royale-{timestamp}.txt",
        )

    final_print(console_logs)
    return world_result, results, console_logs
