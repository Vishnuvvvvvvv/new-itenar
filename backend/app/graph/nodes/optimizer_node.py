from app.graph.state import TravelState

from app.agents.optimizer_agent import (
    optimizer_agent
)


def optimizer_node(
    state: TravelState
):

    flights = state[
        "flight_options"
    ]

    hotels = state[
        "hotel_options"
    ]

    policy_results = state[
        "policy_results"
    ]

    optimized_itinerary = optimizer_agent(

        flights,

        hotels,

        policy_results
    )

    state["optimized_itinerary"] = (
        optimized_itinerary
    )

    state["execution_logs"].append(
        "LLM Optimizer agent executed successfully."
    )

    return state