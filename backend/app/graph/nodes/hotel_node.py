from app.graph.state import (
    TravelState
)

from app.agents.hotel_agent import (
    hotel_agent
)


def hotel_node(
    state: TravelState
):

    parsed = state.get(
        "parsed_request",
        {}
    )

    destinations = parsed.get(
        "destinations",
        []
    )

    preferences = parsed.get(
        "preferences",
        []
    )

    hotels = hotel_agent(

        destinations,
        preferences
    )

    state["hotel_options"] = (
        hotels
    )

    state["execution_logs"].append(
        "Hotel agent executed successfully."
    )

    return state