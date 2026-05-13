from app.graph.state import (
    TravelState
)

from app.agents.transport_agent import (
    transport_agent
)


def transport_node(
    state: TravelState
):

    hotels = state.get(
        "hotel_options",
        []
    )

    cities = list(

        set(

            hotel.get("city")

            for hotel in hotels
        )
    )

    transports = transport_agent(
        cities
    )

    state[
        "transport_options"
    ] = transports

    state[
        "execution_logs"
    ].append(
        "Transport agent executed successfully."
    )

    return state