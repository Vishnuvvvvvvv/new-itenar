from app.utils.json_loader import (
    load_json_file
)


FLIGHT_FILE = (
    "app/mock_server/flights.json"
)


def search_flights(
    source,
    destinations
):

    flights = load_json_file(
        FLIGHT_FILE
    )

    # SUPPORT SINGLE DESTINATION

    if isinstance(
        destinations,
        str
    ):

        destinations = [
            destinations
        ]

    normalized_destinations = [

        destination.lower()

        for destination in destinations
    ]

    matching_flights = []

    for flight in flights:

        if (

            flight.get(
                "source",
                ""
            ).lower()

            == source.lower()

            and

            flight.get(
                "destination",
                ""
            ).lower()

            in normalized_destinations
        ):

            matching_flights.append(
                flight
            )

    return matching_flights