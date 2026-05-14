from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.hotel_agent import (
    hotel_agent
)


def hotel_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Hotel Agent",
        "Searching business hotel options near destination office areas."
    )

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

    warnings = state.get(
        "recommendation_warnings",
        []
    )
    hotel_cities = {
        hotel.get("city")
        for hotel in hotels
    }
    for destination in destinations:
        if destination not in hotel_cities:
            warnings.append(
                f"No mock hotel data found for {destination}."
            )
    state["recommendation_warnings"] = warnings

    run_agent_step(
        state,
        "Hotel Agent",
        f"Selected {len(hotels)} hotel recommendation(s)."
    )

    return state
