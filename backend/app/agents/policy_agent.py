from app.rag.retriever import (
    retrieve_policy
)


HOTEL_NIGHTLY_LIMIT = 8000
TRIP_COST_LIMIT = 25000


def policy_agent(
    flights,
    hotels,
    employee_context,
    total_cost
):
    department = employee_context.get(
        "department",
        ""
    )
    designation = employee_context.get(
        "designation",
        ""
    )

    policy_context = retrieve_policy(
        f"Department: {department}\nDesignation: {designation}\nTravel Policy"
    )

    violations = []
    recommendations = []

    for flight in flights or []:
        if flight.get("travel_class", "").lower() != "economy":
            violations.append(
                {
                    "type": "flight_class",
                    "description": (
                        f"{flight.get('flight_id')} uses "
                        f"{flight.get('travel_class')} class."
                    ),
                }
            )
            recommendations.append(
                "Prefer economy class unless manager approval is available."
            )

    for hotel in hotels or []:
        if hotel.get("hotel_type", "").lower() == "luxury":
            violations.append(
                {
                    "type": "hotel_type",
                    "description": (
                        f"{hotel.get('hotel_name')} is categorized as luxury."
                    ),
                }
            )
        if hotel.get("price_per_night", 0) > HOTEL_NIGHTLY_LIMIT:
            violations.append(
                {
                    "type": "hotel_budget",
                    "description": (
                        f"{hotel.get('hotel_name')} exceeds INR "
                        f"{HOTEL_NIGHTLY_LIMIT} per night."
                    ),
                }
            )

    if total_cost > TRIP_COST_LIMIT:
        violations.append(
            {
                "type": "trip_budget",
                "description": (
                    f"Trip total INR {total_cost} exceeds INR {TRIP_COST_LIMIT}."
                ),
            }
        )

    if violations:
        recommendations.append(
            "Submit this itinerary for manager approval before booking."
        )

    return {
        "compliant": not violations,
        "violations": violations,
        "recommendations": list(dict.fromkeys(recommendations)),
        "policy_context_used": bool(policy_context),
    }
