from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)


def explanation_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Explanation Agent",
        "Preparing conversational summary for the frontend."
    )
    optimized = state.get(
        "optimized_itinerary",
        {}
    )

    policy_results = state.get(
        "policy_results",
        {}
    )

    transport_options = state.get(
        "transport_options",
        []
    )

    approval = state.get(
        "approval_workflow",
        {}
    )

    calendar_analysis = state.get(
        "calendar_analysis",
        {}
    )

    itinerary_days = state.get(
        "itinerary_days",
        []
    )

    selected_flights = optimized.get(
        "selected_flights",
        []
    )

    selected_hotels = optimized.get(
        "selected_hotels",
        []
    )

    response = "Optimized itinerary generated.\n"

    if selected_flights:
        response += "\nSELECTED FLIGHTS:\n"
        for flight in selected_flights:
            response += f"""
{flight.get('airline')}
Route: {flight.get('source')} -> {flight.get('destination')}
Departure: {flight.get('departure_time')}
Arrival: {flight.get('arrival_time')}
Price: INR {flight.get('price')}
Ranking: {flight.get('ranking_score', 'N/A')}/100
"""

    if selected_hotels:
        response += "\nSELECTED HOTELS:\n"
        for hotel in selected_hotels:
            response += f"""
{hotel.get('hotel_name')}
City: {hotel.get('city')}
Location: {hotel.get('location_area')}
Rating: {hotel.get('rating')}
Price/Night: INR {hotel.get('price_per_night')}
Ranking: {hotel.get('ranking_score', 'N/A')}/100
"""

    if transport_options:
        response += "\nLOCAL TRANSPORT:\n"
        for transport in transport_options:
            response += f"""
{transport.get('city')}: {transport.get('transport_type')}
Coverage: {transport.get('coverage_area')}
Cost: INR {transport.get('estimated_cost')}
Ranking: {transport.get('ranking_score', 'N/A')}/100
"""

    response += f"""

TOTAL COST:
INR {optimized.get('total_trip_cost', 0)}

OPTIMIZATION REASON:
{optimized.get('optimization_reason', '')}
"""

    if policy_results.get(
        "compliant",
        True
    ):
        response += "\nTrip is policy compliant.\n"
    else:
        response += "\nPolicy violations detected.\n"

    if approval:
        response += f"""

APPROVAL WORKFLOW:
Approval Required: {approval.get('approval_required')}
Approval Level: {approval.get('approval_level')}
Status: {approval.get('status')}
Reason: {approval.get('reason')}
"""

    if itinerary_days:
        response += "\nDAY-WISE ITINERARY:\n"
        for day in itinerary_days:
            response += (
                f"\nDay {day.get('day')} - "
                f"{day.get('city')} ({day.get('date')})\n"
            )
            for item in day.get("timeline", []):
                response += (
                    f"- {item.get('time')}: "
                    f"{item.get('title')}\n"
                )

    schedule_analysis = []
    if isinstance(calendar_analysis, dict):
        schedule_analysis = calendar_analysis.get(
            "schedule_analysis",
            []
        )

    if schedule_analysis:
        response += "\nSCHEDULE ANALYSIS:\n"
        for item in schedule_analysis:
            response += f"""
City: {item.get('city')}
Meeting Time: {item.get('meeting_time')}
Buffer: {item.get('buffer_minutes')} minutes
Risk: {item.get('risk_level')}
"""

    state[
        "final_response"
    ] = response

    run_agent_step(
        state,
        "Explanation Agent",
        "Final assistant response prepared."
    )

    return state
