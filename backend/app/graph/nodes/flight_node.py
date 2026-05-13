from app.graph.state import (
    TravelState
)

from app.agents.flight_agent import (
    flight_agent
)


def flight_node(
    state: TravelState
):

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

    selected_flights = flight_agent(

        source,
        destinations,
        preferences
    )

    state["flight_options"] = (
        selected_flights
    )

    state["execution_logs"].append(
        "Flight agent executed successfully."
    )

    return state