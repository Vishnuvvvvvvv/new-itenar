from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.policy_agent import (
    policy_agent
)


def policy_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Policy RAG Agent",
        "Validating selected itinerary against enterprise travel policy rules."
    )

    optimized = state.get(
        "optimized_itinerary",
        {}
    )

    flights = optimized.get(
        "selected_flights",
        state.get("flight_options", [])
    )

    hotels = optimized.get(
        "selected_hotels",
        state.get("hotel_options", [])
    )

    employee_context = state.get(
        "employee_context",
        {}
    )

    # =========================
    # CALCULATE TOTAL COST
    # =========================

    total_cost = (
        sum(
            flight.get(
                "price",
                0
            )
            for flight in flights
        )
        +
        sum(
            hotel.get(
                "price_per_night",
                0
            )
            for hotel in hotels
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

    # =========================
    # POLICY AGENT
    # =========================

    results = policy_agent(

        flights,
        hotels,
        employee_context,
        total_cost
    )

    state["policy_results"] = (
        results
    )

    run_agent_step(
        state,
        "Policy RAG Agent",
        "Policy compliance and violations evaluated."
    )

    return state
