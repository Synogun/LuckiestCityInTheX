# City Royale

A simulation to determine the last city standing through a daily elimination process.

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/downloads/release/python-314/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Only requirement is `requests` library.

P.S.: This is was a little fun side project, don't expect production-level code.

## Files

- [main.py](main.py): Main simulation script.
- [data_types.py](data_types.py): Definitions of data structures used in the simulation.
- [src/get_data.py](src/get_data.py): Script used to fetch and store country, state, and city data from an external API.
  - Keep in mind this is only the last edited version; functions used to fetch data may have been modified or removed in the development process.
- [src/data_handler.py](src/data_handler.py): Utility functions for reading and writing JSON files.
- [src/simulation.py](src/simulation.py): Core simulation logic and functions.
- [src/analysis.py](src/analysis.py): Functions for analyzing and visualizing simulation results.
- [data/](data/): Directory containing JSON data files for countries, states, and cities.
  - Check [Data Sources](#data-sources) for more information.
- [logs/](logs/): Directory for storing simulation logs.
- [reqs.txt](reqs.txt): List of Python dependencies.

## Data Sources

- [data/world_countries.json](data/world_countries.json) -> https://docs.countrystatecity.in/api/endpoints/get-all-countries
- [data/world_countries_details.json](data/world_countries_details.json) -> https://docs.countrystatecity.in/api/endpoints/get-country-details
- [data/full_world_countries.json](data/full_world_countries.json) -> Combination of 'world_countries.json' and 'world_countries_details.json'
- [data/world_states.json](data/world_states.json) -> https://docs.countrystatecity.in/api/endpoints/get-all-states
- [data/world_cities.json](data/world_cities.json) -> https://docs.countrystatecity.in/api/endpoints/get-cities-by-country
