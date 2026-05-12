from app.graph.state import TravelState

from app.agents.parser_agent import (
    parser_agent
)


def parser_node(state: TravelState):

    user_input = state["user_input"]

    parsed_request = parser_agent(
        user_input
    )

    state["parsed_request"] = parsed_request

    state["execution_logs"].append(
        "LLM Parser Agent executed successfully."
    )

    return state