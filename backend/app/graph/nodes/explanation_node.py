from app.graph.state import (
    TravelState
)


def explanation_node(
    state: TravelState
):

    itinerary = state[
        "optimized_itinerary"
    ]

    policy_results = state[
        "policy_results"
    ]

    compliant = policy_results.get(
        "compliant",
        True
    )

    response = "\n"

    response += (
        "Optimized itinerary generated.\n\n"
    )

    # =========================
    # FLIGHT
    # =========================

    response += (
        "Selected Flight:\n"
    )

    response += (
        f"{itinerary['selected_flight'].get('airline', 'N/A')}"
        "\n\n"
    )

    # =========================
    # HOTEL
    # =========================

    response += (
        "Selected Hotel:\n"
    )

    response += (
        f"{itinerary['selected_hotel'].get('hotel_name', 'N/A')}"
        "\n\n"
    )

    # =========================
    # COST
    # =========================

    response += (
        "Total Cost:\n"
    )

    response += (
        f"₹{itinerary.get('total_trip_cost', 0)}"
        "\n\n"
    )

    # =========================
    # OPTIMIZATION REASON
    # =========================

    response += (
        "Optimization Reason:\n"
    )

    response += (
        f"{itinerary.get('optimization_reason', '')}"
        "\n\n"
    )

    # =========================
    # COMPLIANCE
    # =========================

    if compliant:

        response += (
            "Trip is policy compliant.\n"
        )

    else:

        response += (
            "Policy violations detected.\n"
        )

    state["final_response"] = (
        response
    )

    state["execution_logs"].append(
        "Explanation node executed."
    )

    return state