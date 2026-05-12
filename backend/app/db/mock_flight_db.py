from app.utils.json_loader import (
    load_json_file
)


FLIGHT_FILE = "app/mock_server/flights.json"


def get_flights(

    source,

    destination
):

    flights = load_json_file(
        FLIGHT_FILE
    )

    matching_flights = []

    for flight in flights:

        if (

            flight.get("source", "").lower()

            == source.lower()

            and

            flight.get(
                "destination",
                ""
            ).lower()

            == destination.lower()
        ):

            matching_flights.append(
                flight
            )

    return matching_flights