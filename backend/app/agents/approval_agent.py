APPROVAL_COST_THRESHOLD = 25000


def approval_agent(

    optimized_itinerary,

    policy_results
):

    selected_flights = optimized_itinerary.get(
        "selected_flights",
        []
    )

    selected_hotels = optimized_itinerary.get(
        "selected_hotels",
        []
    )

    total_trip_cost = optimized_itinerary.get(
        "total_trip_cost",
        0
    )

    reasons = []
    violations = policy_results.get(
        "violations",
        []
    ) or []

    if not policy_results.get("compliant", True) or violations:
        reasons.append("Policy violations detected.")

    if total_trip_cost > APPROVAL_COST_THRESHOLD:
        reasons.append(
            f"Total trip cost exceeds INR {APPROVAL_COST_THRESHOLD}."
        )

    if any(
        flight.get("travel_class", "").lower() == "business"
        for flight in selected_flights
    ):
        reasons.append("Business class flight selected.")

    if any(
        hotel.get("hotel_type", "").lower() == "luxury"
        for hotel in selected_hotels
    ):
        reasons.append("Luxury hotel selected.")

    approval_required = bool(reasons)

    if not approval_required:
        return {
            "approval_required": False,
            "approval_level": "None",
            "status": "not_required",
            "approval_completed": True,
            "reason": "Trip is within deterministic approval rules.",
            "violations": [],
        }

    return {
        "approval_required": True,
        "approval_level": "Manager",
        "status": "pending",
        "approval_completed": False,
        "reason": " ".join(reasons),
        "violations": violations,
    }
