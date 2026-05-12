from app.graph.state import TravelState

from app.db.mock_flight_db import (
    get_flights
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

    employee_context = state.get(
        "employee_context",
        {}
    )

    preferences = parsed_request.get(
        "preferences",
        []
    )

    destination = parsed_request.get(
        "destination",
        ""
    )

    employee_location = employee_context.get(
        "employee_location",
        ""
    )

    # =========================
    # FETCH FLIGHTS
    # =========================

    flights = get_flights(

        employee_location,

        destination
    )

    # =========================
    # ENSURE VALID LIST
    # =========================

    if not isinstance(
        flights,
        list
    ):

        flights = []

    # =========================
    # LLM FILTERING
    # =========================

    recommended_flights = flight_agent(

        preferences,

        flights,

        employee_context
    )

    # =========================
    # FINAL SAFETY
    # =========================

    if not isinstance(
        recommended_flights,
        list
    ):

        recommended_flights = flights

    state["flight_options"] = (
        recommended_flights
    )

    state["execution_logs"].append(
        "Flight agent executed successfully."
    )

    return state