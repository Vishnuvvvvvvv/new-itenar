from app.graph.state import TravelState
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.supervisor_agent import (
    supervisor_agent
)


def supervisor_node(state: TravelState):
    run_agent_step(
        state,
        "Supervisor Agent",
        "Classifying request and selecting downstream travel agents."
    )

    parsed_request = state["parsed_request"]

    user_input = state["user_input"]

    result = supervisor_agent(
        parsed_request,
        user_input
    )

    state["request_type"] = result[
        "request_type"
    ]

    state["next_steps"] = result[
        "next_steps"
    ]

    run_agent_step(
        state,
        "Supervisor Agent",
        f"Workflow selected: {', '.join(result.get('next_steps', []))}."
    )

    return state
