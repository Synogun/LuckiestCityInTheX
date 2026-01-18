from src.simulation import country_city_royale


def run_until_my_city_wins(
    country_name: str,
    my_city_name: str,
    threshold: int | None = None,
) -> int:
    """Runs simulations until the specified city wins, returning the number of attempts."""

    attempts = 0
    while True:
        attempts += 1
        _, results, console_logs = country_city_royale(
            starting_date=None,
            country_name=country_name,
            my_city_name=my_city_name,
            save_to_file=False,
            print_to_console=False,
        )

        ultimate_winner_info = results[0][1]
        if my_city_name.lower() == ultimate_winner_info["name"].lower():
            print(f"{my_city_name} won after {attempts} attempts!")

            print("Winning result details:")
            print("\n".join(console_logs))
            break

        if threshold is not None and 0 < threshold == attempts:
            print(
                f"After {attempts} attempts, "
                + f"{my_city_name} did not win. Stopping Now.",
            )
            break

        if attempts % 100 == 0:
            print(f"Attempts so far: {attempts}")

    return attempts
