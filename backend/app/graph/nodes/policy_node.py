from app.graph.state import TravelState

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

    # =========================
    # SAFE ACCESS
    # =========================

    selected_flight = (

        flights[0]

        if isinstance(flights, list)
        and len(flights) > 0

        else {}
    )

    selected_hotel = (

        hotels[0]

        if isinstance(hotels, list)
        and len(hotels) > 0

        else {}
    )

    policy_result = policy_agent(

        selected_flight,

        selected_hotel
    )

    state["policy_results"] = (
        policy_result
    )

    state["execution_logs"].append(
        "Policy RAG agent executed successfully."
    )

    return state