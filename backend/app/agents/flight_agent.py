from app.db.mock_flight_db import (
    search_flights
)


def flight_agent(
    source,
    destinations,
    preferences
):
    selected_flights = []
    current_source = source
    preference_text = " ".join(
        str(item).lower()
        for item in preferences or []
    )

    for destination in destinations:
        available_flights = search_flights(
            current_source,
            destination
        )

        if available_flights:
            selected_flights.append(
                _select_best_flight(
                    available_flights,
                    preference_text
                )
            )

        current_source = destination

    return selected_flights


def _select_best_flight(
    flights,
    preference_text
):
    ranked = sorted(
        flights,
        key=lambda flight: (
            _morning_penalty(flight, preference_text),
            flight.get("travel_class", "") != "economy",
            flight.get("stops", 99),
            flight.get("price", 999999),
        )
    )

    selected = dict(ranked[0])
    selected["reason"] = (
        "Deterministic selection based on timing preference, economy class, "
        "fewer stops, and lower cost."
    )
    return selected


def _morning_penalty(
    flight,
    preference_text
):
    if "avoid morning" not in preference_text and "no morning" not in preference_text:
        return 0

    departure = str(
        flight.get("departure_time", "")
    ).lower()

    if "am" not in departure:
        return 0

    try:
        hour = int(
            departure.split(":")[0]
        )
    except Exception:
        return 0

    return 1 if hour < 12 else 0
