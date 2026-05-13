from app.graph.state import (
    TravelState
)


def explanation_node(
    state: TravelState
):

    optimized = state.get(
        "optimized_itinerary",
        {}
    )

    policy_results = state.get(
        "policy_results",
        {}
    )

    transport = state.get(
        "transport_recommendation",
        {}
    )

    approval = state.get(
        "approval_workflow",
        {}
    )

    calendar_analysis = state.get(
        "calendar_analysis",
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

    response = (
        "\nOptimized itinerary generated.\n"
    )

    response += "\n\nSELECTED FLIGHTS:\n"

    for flight in selected_flights:

        response += f"""

{flight.get('airline')}
Route: {flight.get('source')} → {flight.get('destination')}
Departure: {flight.get('departure_time')}
Arrival: {flight.get('arrival_time')}
Price: ₹{flight.get('price')}
"""

    response += "\nSELECTED HOTELS:\n"

    for hotel in selected_hotels:

        response += f"""

{hotel.get('hotel_name')}
City: {hotel.get('city')}
Location: {hotel.get('location_area')}
Rating: {hotel.get('rating')}
Price/Night: ₹{hotel.get('price_per_night')}
"""

    response += f"""

TOTAL COST:
₹{optimized.get('total_trip_cost', 0)}

OPTIMIZATION REASON:
{optimized.get('optimization_reason', '')}
"""

    if policy_results.get(
        "compliant"
    ):

        response += (
            "\n\nTrip is policy compliant.\n"
        )

    else:

        response += (
            "\n\nPolicy violations detected.\n"
        )

    if transport:

        response += f"""

LOCAL TRANSPORT:

Transport Type:
{transport.get('selected_transport_type')}

Reason:
{transport.get('reason')}
"""

    if approval:

        response += f"""

APPROVAL WORKFLOW:

Approval Required:
{approval.get('approval_required')}

Approval Level:
{approval.get('approval_level')}

Reason:
{approval.get('reason')}
"""

    if calendar_analysis:

        response += (
            "\n\nSCHEDULE ANALYSIS:\n"
        )

        for item in calendar_analysis:

            response += f"""

City: {item.get('city')}
Meeting: {item.get('meeting_title')}
Arrival: {item.get('arrival_time')}
Meeting Time: {item.get('meeting_time')}
Buffer: {item.get('buffer_minutes')} minutes
"""

    state[
        "final_response"
    ] = response

    state[
        "execution_logs"
    ].append(
        "Explanation node executed."
    )

    return state