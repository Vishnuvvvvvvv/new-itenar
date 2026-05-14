def optimizer_agent(
    flights,
    hotels,
    policy_results,
    calendar_analysis
):
    selected_flights = _select_one_per_route(
        flights
    )

    selected_hotels = _select_one_per_city(
        hotels
    )

    total_cost = (
        sum(
            flight.get("price", 0)
            for flight in selected_flights
        )
        +
        sum(
            hotel.get("price_per_night", 0)
            for hotel in selected_hotels
        )
    )

    return {
        "selected_flights": selected_flights,
        "selected_hotels": selected_hotels,
        "optimization_reason": (
            "Deterministic optimizer selected the highest-ranked available "
            "flight for each route and hotel for each city."
        ),
        "total_trip_cost": total_cost,
    }


def _select_one_per_route(
    flights
):
    selected = []
    covered_routes = set()

    for flight in sorted(
        flights or [],
        key=lambda item: (
            -item.get("ranking_score", 0),
            item.get("price", 999999),
        )
    ):
        route = (
            f"{flight.get('source')}"
            f"->{flight.get('destination')}"
        )
        if route not in covered_routes:
            selected.append(flight)
            covered_routes.add(route)

    return selected


def _select_one_per_city(
    hotels
):
    selected = []
    covered_cities = set()

    for hotel in sorted(
        hotels or [],
        key=lambda item: (
            -item.get("ranking_score", 0),
            item.get("price_per_night", 999999),
        )
    ):
        city = hotel.get("city")
        if city not in covered_cities:
            selected.append(hotel)
            covered_cities.add(city)

    return selected
