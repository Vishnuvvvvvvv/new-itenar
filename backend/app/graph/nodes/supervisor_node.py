from app.graph.state import TravelState

from app.agents.supervisor_agent import (
    supervisor_agent
)


def supervisor_node(state: TravelState):

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

    state["execution_logs"].append(
        "LLM Supervisor Agent executed successfully."
    )

    return state