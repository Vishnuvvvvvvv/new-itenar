from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.flight_agent import (
    flight_agent
)


def flight_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Flight Agent",
        "Searching mock flight inventory and applying timing, class, stop, and cost preferences."
    )

    parsed_request = state.get(
        "parsed_request",
        {}
    )

    source = parsed_request.get(
        "source",
        ""
    )

    destinations = parsed_request.get(
        "destinations",
        []
    )

    preferences = parsed_request.get(
        "preferences",
        []
    )

    employee_context = state.get(
        "employee_context",
        {}
    )

    if not source:
        source = employee_context.get(
            "employee_location",
            ""
        )
        parsed_request["source"] = source

    destinations = [
        destination for destination in destinations
        if destination and destination.lower() != source.lower()
    ]
    parsed_request["destinations"] = destinations
    state["parsed_request"] = parsed_request

    selected_flights = flight_agent(

        source,
        destinations,
        preferences
    )

    state["flight_options"] = (
        selected_flights
    )

    warnings = state.get(
        "recommendation_warnings",
        []
    )
    available_routes = {
        (
            flight.get("source"),
            flight.get("destination")
        )
        for flight in selected_flights
    }
    current_source = source
    for destination in destinations:
        if (
            current_source,
            destination
        ) not in available_routes:
            warnings.append(
                f"No mock flight data found for {current_source} to {destination}."
            )
        current_source = destination

    state["recommendation_warnings"] = warnings

    run_agent_step(
        state,
        "Flight Agent",
        f"Selected {len(selected_flights)} flight recommendation(s)."
    )

    return state
