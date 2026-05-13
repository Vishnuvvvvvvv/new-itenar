from app.graph.state import (
    TravelState
)

from app.agents.optimizer_agent import (
    optimizer_agent
)


def optimizer_node(
    state: TravelState
):

    flights = state.get(
        "flight_options",
        []
    )

    hotels = state.get(
        "hotel_options",
        []
    )

    policy_results = state.get(
        "policy_results",
        {}
    )

    calendar_analysis = state.get(
        "calendar_analysis",
        []
    )

    optimized = optimizer_agent(

        flights,
        hotels,
        policy_results,
        calendar_analysis
    )

    state[
        "optimized_itinerary"
    ] = optimized

    state[
        "execution_logs"
    ].append(
        "LLM Optimizer agent executed successfully."
    )

    return state