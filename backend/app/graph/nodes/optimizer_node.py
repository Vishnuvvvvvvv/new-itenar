from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.optimizer_agent import (
    optimizer_agent
)


def optimizer_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Optimizer Agent",
        "Combining ranked recommendations into an optimized multi-city itinerary."
    )

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

    optimized["selected_transports"] = state.get(
        "transport_options",
        []
    )

    optimized["total_trip_cost"] = (
        optimized.get(
            "total_trip_cost",
            0
        )
        +
        sum(
            transport.get(
                "estimated_cost",
                0
            )
            for transport in state.get(
                "transport_options",
                []
            )
        )
    )

    state[
        "optimized_itinerary"
    ] = optimized

    run_agent_step(
        state,
        "Optimizer Agent",
        "Optimized itinerary and total cost calculated."
    )

    return state
