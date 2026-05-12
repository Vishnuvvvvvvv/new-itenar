from app.utils.json_loader import (
    load_json_file
)


HOTEL_FILE = (
    "app/mock_server/hotels.json"
)


def search_hotels(city):

    all_hotels = load_json_file(
        HOTEL_FILE
    )

    matching_hotels = []

    for hotel in all_hotels:

        if (
            hotel["city"].lower()
            == city.lower()
        ):

            matching_hotels.append(
                hotel
            )

    return matching_hotels