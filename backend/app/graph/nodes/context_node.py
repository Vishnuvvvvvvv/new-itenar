from app.graph.state import TravelState
from app.graph.agent_runtime import (
    run_agent_step
)

from app.db.mock_employee_db import (
    get_employee
)


def context_node(state: TravelState):
    run_agent_step(
        state,
        "Context Agent",
        "Loading employee profile and enterprise travel context."
    )

    employee_id = state[
        "employee_id"
    ]

    employee = get_employee(
        employee_id
    )

    state["employee_context"] = employee

    run_agent_step(
        state,
        "Context Agent",
        "Employee context loaded."
    )

    return state
