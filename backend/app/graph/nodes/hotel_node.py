from app.graph.state import TravelState

from app.agents.hotel_agent import (
    hotel_agent
)


def hotel_node(state: TravelState):

    parsed_request = state[
        "parsed_request"
    ]

    hotels = hotel_agent(
        parsed_request
    )

    state["hotel_options"] = hotels

    state["execution_logs"].append(
        "Hotel agent executed successfully."
    )

    return state