from datetime import datetime, timedelta
from typing import Any, Dict, List


def build_day_wise_itinerary(
    parsed_request: Dict[str, Any],
    optimized_itinerary: Dict[str, Any],
    transports: List[Dict[str, Any]],
    calendar_analysis: Dict[str, Any],
    policy_results: Dict[str, Any],
    approval_workflow: Dict[str, Any],
) -> List[Dict[str, Any]]:
    destinations = parsed_request.get("destinations", []) or []
    meetings = parsed_request.get("meetings", []) or []
    flights = optimized_itinerary.get("selected_flights", []) or []
    hotels = optimized_itinerary.get("selected_hotels", []) or []
    schedule = calendar_analysis.get("schedule_analysis", []) if isinstance(calendar_analysis, dict) else []
    start_date = _parse_date(parsed_request.get("start_date"))

    days = []
    for index, city in enumerate(destinations):
        date = _date_for_city(start_date, meetings, city, index)
        timeline = []

        flight = _find_flight_to_city(flights, city)
        if flight:
            timeline.append(
                {
                    "type": "flight",
                    "title": f"{flight.get('source')} to {flight.get('destination')}",
                    "time": flight.get("departure_time", "TBD"),
                    "details": f"{flight.get('airline')} {flight.get('flight_id')} arrives {flight.get('arrival_time')}",
                    "cost": flight.get("price", 0),
                    "status": "selected",
                }
            )

        transport = _find_by_city(transports, city)
        if transport:
            timeline.append(
                {
                    "type": "transport",
                    "title": f"{transport.get('transport_type')} to office or hotel",
                    "time": "After arrival",
                    "details": f"{transport.get('coverage_area')} coverage, {transport.get('comfort_level')} comfort",
                    "cost": transport.get("estimated_cost", 0),
                    "status": "selected",
                }
            )

        hotel = _find_by_city(hotels, city)
        if hotel:
            timeline.append(
                {
                    "type": "hotel",
                    "title": f"Check in at {hotel.get('hotel_name')}",
                    "time": "Evening",
                    "details": f"{hotel.get('location_area')} · rating {hotel.get('rating')}",
                    "cost": hotel.get("price_per_night", 0),
                    "status": "selected",
                }
            )

        for meeting in _meetings_for_city(meetings, city):
            timeline.append(
                {
                    "type": "meeting",
                    "title": meeting.get("title") or meeting.get("meeting_title") or "Business meeting",
                    "time": meeting.get("time") or meeting.get("meeting_time") or "TBD",
                    "details": meeting.get("location") or meeting.get("office_location") or city,
                    "status": "scheduled",
                }
            )

        for item in _meetings_for_city(schedule, city):
            timeline.append(
                {
                    "type": "calendar",
                    "title": "Schedule feasibility",
                    "time": item.get("meeting_time", "TBD"),
                    "details": f"Buffer {item.get('buffer_minutes', 0)} mins · risk {item.get('risk_level', 'unknown')}",
                    "status": "feasible" if item.get("feasible", True) else "risk",
                }
            )

        if index == len(destinations) - 1:
            timeline.append(
                {
                    "type": "policy",
                    "title": "Policy and approval status",
                    "time": "Trip review",
                    "details": _status_summary(policy_results, approval_workflow),
                    "status": approval_workflow.get("status", "not_required"),
                }
            )

        days.append(
            {
                "day": index + 1,
                "date": date,
                "city": city,
                "timeline": timeline,
            }
        )

    return days


def _parse_date(value):
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _date_for_city(start_date, meetings, city, index):
    for meeting in _meetings_for_city(meetings, city):
        if meeting.get("date") or meeting.get("meeting_date"):
            return meeting.get("date") or meeting.get("meeting_date")
    if start_date:
        return (start_date + timedelta(days=index)).strftime("%Y-%m-%d")
    return f"Day {index + 1}"


def _find_flight_to_city(flights, city):
    for flight in flights:
        if str(flight.get("destination", "")).lower() == str(city).lower():
            return flight
    return None


def _find_by_city(items, city):
    for item in items or []:
        if str(item.get("city", "")).lower() == str(city).lower():
            return item
    return None


def _meetings_for_city(items, city):
    return [
        item for item in items or []
        if str(item.get("city", "")).lower() == str(city).lower()
    ]


def _status_summary(policy_results, approval_workflow):
    if policy_results.get("compliant", True):
        return "Policy compliant. No approval required."
    return (
        f"Policy violations found. Approval status: "
        f"{approval_workflow.get('status', 'pending')}."
    )
