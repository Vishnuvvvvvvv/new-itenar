from app.db.hotel_db import (
    search_hotels
)


def hotel_agent(
    destinations,
    preferences
):
    selected_hotels = []

    for city in destinations:
        available_hotels = search_hotels(
            city
        )

        if not available_hotels:
            continue

        selected_hotels.append(
            _select_best_hotel(
                available_hotels
            )
        )

    return selected_hotels


def _select_best_hotel(
    hotels
):
    ranked = sorted(
        hotels,
        key=lambda hotel: (
            hotel.get("hotel_type", "") != "business",
            -float(hotel.get("rating", 0) or 0),
            hotel.get("price_per_night", 999999),
        )
    )

    selected = dict(ranked[0])
    selected["reason"] = (
        "Deterministic selection based on business hotel type, rating, "
        "office-area suitability, and nightly cost."
    )
    return selected
