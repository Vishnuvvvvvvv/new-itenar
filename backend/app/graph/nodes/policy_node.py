from app.graph.state import (
    TravelState
)

from app.agents.policy_agent import (
    policy_agent
)


def policy_node(
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

    state[
        "execution_logs"
    ].append(
        "Policy RAG agent executed successfully."
    )

    return state