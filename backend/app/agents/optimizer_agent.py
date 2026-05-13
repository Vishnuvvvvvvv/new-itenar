import json

from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


def optimizer_agent(

    flights,
    hotels,
    policy_results,
    calendar_analysis
):

    # =========================
    # BUILD REQUIRED ROUTES
    # =========================

    required_routes = []

    for flight in flights:

        route = (

            f"{flight.get('source')}"
            f"->{flight.get('destination')}"
        )

        if route not in required_routes:

            required_routes.append(
                route
            )

    # =========================
    # BUILD REQUIRED CITIES
    # =========================

    required_cities = []

    for hotel in hotels:

        city = hotel.get(
            "city"
        )

        if city not in required_cities:

            required_cities.append(
                city
            )

    prompt = f"""
You are an enterprise itinerary optimizer agent.

TASK:

1. Select EXACTLY ONE BEST FLIGHT
   for EACH REQUIRED ROUTE

2. Select EXACTLY ONE BEST HOTEL
   for EACH REQUIRED CITY

3. NEVER skip:
   - any route
   - any city

4. Prioritize:
   - policy compliance
   - business convenience
   - fewer stops
   - economy class
   - reasonable pricing
   - higher ratings
   - office proximity

5. Avoid:
   - morning flights
   - policy violations
   - expensive hotels

IMPORTANT:

- MULTI CITY COVERAGE IS MANDATORY
- ALL ROUTES MUST HAVE FLIGHTS
- ALL CITIES MUST HAVE HOTELS

Return STRICT JSON ONLY.

DO NOT explain.
DO NOT add markdown.
DO NOT generate code.

OUTPUT FORMAT:

{{
  "selected_flight_ids": [],
  "selected_hotel_ids": [],
  "reason": ""
}}

=========================
REQUIRED ROUTES
=========================

{json.dumps(required_routes, indent=2)}

=========================
REQUIRED HOTEL CITIES
=========================

{json.dumps(required_cities, indent=2)}

=========================
AVAILABLE FLIGHTS
=========================

{json.dumps(flights, indent=2)}

=========================
AVAILABLE HOTELS
=========================

{json.dumps(hotels, indent=2)}

=========================
POLICY RESULTS
=========================

{json.dumps(policy_results, indent=2)}

=========================
CALENDAR ANALYSIS
=========================

{json.dumps(calendar_analysis, indent=2)}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nOPTIMIZER RAW OUTPUT:\n"
        )

        print(content)

        result = extract_json(
            content
        )

        selected_flight_ids = result.get(
            "selected_flight_ids",
            []
        )

        selected_hotel_ids = result.get(
            "selected_hotel_ids",
            []
        )

        # =========================
        # LLM SELECTED FLIGHTS
        # =========================

        selected_flights = []

        covered_routes = set()

        for flight in flights:

            if (

                flight.get(
                    "flight_id"
                )

                in selected_flight_ids
            ):

                selected_flights.append(
                    flight
                )

                route = (

                    f"{flight.get('source')}"
                    f"->{flight.get('destination')}"
                )

                covered_routes.add(
                    route
                )

        # =========================
        # ENFORCE ROUTE COVERAGE
        # =========================

        for route in required_routes:

            if route not in covered_routes:

                source, destination = (
                    route.split("->")
                )

                matching = [

                    flight

                    for flight in flights

                    if (

                        flight.get(
                            "source"
                        ) == source

                        and

                        flight.get(
                            "destination"
                        ) == destination
                    )
                ]

                if matching:

                    selected_flights.append(
                        matching[0]
                    )

        # =========================
        # LLM SELECTED HOTELS
        # =========================

        selected_hotels = []

        covered_cities = set()

        for hotel in hotels:

            if (

                hotel.get(
                    "hotel_id"
                )

                in selected_hotel_ids
            ):

                selected_hotels.append(
                    hotel
                )

                covered_cities.add(
                    hotel.get("city")
                )

        # =========================
        # ENFORCE CITY COVERAGE
        # =========================

        for city in required_cities:

            if city not in covered_cities:

                matching = [

                    hotel

                    for hotel in hotels

                    if hotel.get(
                        "city"
                    ) == city
                ]

                if matching:

                    selected_hotels.append(
                        matching[0]
                    )

        # =========================
        # TOTAL COST
        # =========================

        total_cost = (

            sum(

                flight.get(
                    "price",
                    0
                )

                for flight in selected_flights
            )

            +

            sum(

                hotel.get(
                    "price_per_night",
                    0
                )

                for hotel in selected_hotels
            )
        )

        return {

            "selected_flights":
            selected_flights,

            "selected_hotels":
            selected_hotels,

            "optimization_reason":
            result.get(
                "reason",
                ""
            ),

            "total_trip_cost":
            total_cost
        }

    except Exception as e:

        print(
            "\nOPTIMIZER ERROR:\n"
        )

        print(str(e))

        return {

            "selected_flights": [],

            "selected_hotels": [],

            "optimization_reason":
            "Fallback optimizer used.",

            "total_trip_cost": 0
        }