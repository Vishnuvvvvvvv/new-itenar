from app.graph.state import (
    TravelState
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

    parsed_input = state.get(
        "parsed_input",
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

    results = calendar_agent(

        meetings,
        flights,
        existing_calendar
    )

    state[
        "calendar_analysis"
    ] = results

    state[
        "execution_logs"
    ].append(
        "Calendar intelligence executed successfully."
    )

    return state