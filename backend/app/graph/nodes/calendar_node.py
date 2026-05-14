from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.calendar_agent import (
    calendar_agent
)

from app.db.mock_calendar_db import (
    get_employee_calendar
)


def calendar_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Calendar Agent",
        "Checking meeting feasibility, arrival buffers, and employee calendar events."
    )

    parsed_input = state.get(
        "parsed_request",
        {}
    )

    employee_context = state.get(
        "employee_context",
        {}
    )

    employee_id = employee_context.get(
        "employee_id"
    )

    meetings = parsed_input.get(
        "meetings",
        []
    )

    flights = state.get(
        "flight_options",
        []
    )

    existing_calendar = (
        get_employee_calendar(
            employee_id
        )
    )

    destinations = [
        city.lower()
        for city in parsed_input.get(
            "destinations",
            []
        )
    ]

    if not meetings:
        meetings = [
            item for item in existing_calendar
            if item.get("city", "").lower() in destinations
        ]
        parsed_input["meetings"] = meetings
        state["parsed_request"] = parsed_input
    elif destinations:
        meetings = [
            item for item in meetings
            if item.get("city", "").lower() in destinations
        ]
        parsed_input["meetings"] = meetings
        state["parsed_request"] = parsed_input

    results = calendar_agent(

        meetings,
        flights,
        existing_calendar
    )

    state[
        "calendar_analysis"
    ] = results

    run_agent_step(
        state,
        "Calendar Agent",
        "Schedule feasibility analysis completed."
    )

    return state
