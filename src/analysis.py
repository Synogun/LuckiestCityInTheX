from datetime import date
from typing import Any

from .simulation import SimulationResult


def find_city(
    results: SimulationResult,
    city_name: str,
) -> tuple[int | None, date | None]:
    """Finds the elimination date of a specific city."""
    for index, (cdate, cinfo) in enumerate(results, start=1):
        if city_name.lower() == cinfo["name"].lower():
            return index, cdate
    return None, None


def do_tracked_city_analysis(
    results: SimulationResult,
    tracked_city_name: str,
    pool_name: str,
    ultimate_loser_name: str,
    ultimate_winner_name: str,
) -> tuple[dict[str, Any], list[str]]:
    """Generates analysis lines for a specific city."""

    analysis_lines: list[str] = []
    tracked_city_result: dict[str, Any] = {"city_name": tracked_city_name}
    tracked_city_index, tracked_city_date = find_city(results, tracked_city_name)

    if tracked_city_date:
        msg = f"{tracked_city_name} is the ULTIMATE {pool_name.upper()}"
        if tracked_city_name.lower() == ultimate_winner_name.lower():
            tracked_city_result["outcome"] = "winner"
            analysis_lines.append(f"{msg} WINNER! :D")

        elif tracked_city_name.lower() == ultimate_loser_name.lower():
            tracked_city_result["outcome"] = "loser"
            analysis_lines.append(f"{msg} LOSER :O")

        else:
            tracked_city_result["outcome"] = "eliminated"

            tracked_city_result["elimination_index"] = tracked_city_index
            tracked_city_result["elimination_date"] = tracked_city_date.strftime(
                "%Y-%m-%d"
            )

            analysis_lines.append(
                f"{tracked_city_index}º {tracked_city_name} was eliminated "
                + f"on {tracked_city_date.strftime('%d-%m-%Y')}"
            )
    else:
        tracked_city_result["outcome"] = "not_found"
        analysis_lines.append(f"{tracked_city_name} was not found in the results.")
    analysis_lines.append("")

    return tracked_city_result, analysis_lines


def analyze_pool_results(
    results: SimulationResult,
    pool_name: str,
    tracked_name: str | None = None,
) -> tuple[dict[str, Any], str]:
    """Analyzes the results of the city elimination and returns a formatted string."""

    if not results:
        return {}, "No results to analyze."

    ultimate_winner_date, ultimate_winner_info = results[0][0], results[0][1]
    ultimate_loser_date, ultimate_loser_info = results[-1][0], results[-1][1]

    analysis_lines: list[str] = []
    analysis_result: dict[str, Any] = {
        "name": pool_name,
        "total_cities": str(len(results)),
        "winner": ultimate_winner_info,
        "loser": ultimate_loser_info,
        "start_date": ultimate_loser_date.strftime("%Y-%m-%d"),
        "end_date": ultimate_winner_date.strftime("%Y-%m-%d"),
    }

    if tracked_name:
        analysis_lines.append("\n--- Tracked City Analysis ---")
        tracked_city_result, analysis_lines_city = do_tracked_city_analysis(
            results,
            tracked_name,
            pool_name,
            ultimate_loser_info["name"],
            ultimate_winner_info["name"],
        )

        analysis_result["tracked_city_analysis"] = tracked_city_result
        analysis_lines.extend(analysis_lines_city)

    analysis_lines.append(f"--- Overall Analysis ---")

    analysis_lines.append(
        f"ULTIMATE {pool_name.upper()} WINNER: "
        + f"{ultimate_winner_info['name']} on "
        + ultimate_winner_date.strftime("%d-%m-%Y")
    )
    analysis_lines.append(
        f"ULTIMATE {pool_name.upper()} LOSER: "
        + f"{ultimate_loser_info['name']} on "
        + ultimate_loser_date.strftime("%d-%m-%Y")
    )

    return analysis_result, "\n".join(analysis_lines)
