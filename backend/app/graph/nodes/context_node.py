from app.graph.state import TravelState

from app.db.mock_employee_db import (
    get_employee
)


def context_node(state: TravelState):

    employee_id = state[
        "employee_id"
    ]

    employee = get_employee(
        employee_id
    )

    state["employee_context"] = employee

    state["execution_logs"].append(
        "Employee context loaded."
    )

    return state