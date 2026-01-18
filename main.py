from src.simulation import global_city_royale

if __name__ == "__main__":
    # country_city_royale(
    #     starting_date=None,
    #     country_name="Canada",
    #     my_city_name="Vancouver",
    #     save_to_file=True,
    #     print_to_console=True,
    # )

    global_city_royale(
        tracked_city_name="Vancouver",
        save_to_file=True,
        print_to_console=True,
        draw_simultaneous_countries=False,
    )
