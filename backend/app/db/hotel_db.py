from app.utils.json_loader import (
    load_json_file
)


HOTEL_FILE = (
    "app/mock_server/hotels.json"
)


def search_hotels(
    cities
):

    hotels = load_json_file(
        HOTEL_FILE
    )

    # SINGLE CITY SUPPORT

    if isinstance(
        cities,
        str
    ):

        cities = [
            cities
        ]

    normalized_cities = [

        city.lower()

        for city in cities
    ]

    matching_hotels = [

        hotel

        for hotel in hotels

        if hotel.get(
            "city",
            ""
        ).lower()

        in normalized_cities
    ]

    return matching_hotels