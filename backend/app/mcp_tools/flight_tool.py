from app.utils.json_loader import (
    load_json_file
)


FLIGHT_FILE = (
    "app/mock_server/flights.json"
)


def search_flights(
    source,
    destination
):

    all_flights = load_json_file(
        FLIGHT_FILE
    )

    matching_flights = []

    for flight in all_flights:

        if (
            flight["source"].lower()
            == source.lower()
            and
            flight["destination"].lower()
            == destination.lower()
        ):

            matching_flights.append(
                flight
            )

    return matching_flights