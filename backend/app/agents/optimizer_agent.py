import json
import re

from app.core.llm import llm


OPTIMIZER_PROMPT = """
You are an enterprise AI itinerary optimization agent.

Your responsibilities:
1. Analyze compliant flight options
2. Analyze compliant hotel options
3. Select BEST itinerary

Optimization priorities:
- policy compliance
- business convenience
- user preferences
- reasonable pricing
- higher ratings
- fewer stops

IMPORTANT:
- Use ONLY provided flight IDs
- Use ONLY provided hotel IDs
- Do NOT invent IDs
- Return ONLY valid JSON
- No markdown
- No explanations
- No Python code

Format:

{{
    "selected_flight_id": "",
    "selected_hotel_id": "",
    "reason": ""
}}

Compliant Flight Options:
{flights}

Compliant Hotel Options:
{hotels}

Policy Results:
{policy_results}
"""


def optimizer_agent(

    flights,

    hotels,

    policy_results
):

    # =========================
    # TYPE SAFETY
    # =========================

    safe_flights = []

    for flight in flights:

        if isinstance(flight, dict):

            safe_flights.append(
                flight
            )

    flights = safe_flights

    safe_hotels = []

    for hotel in hotels:

        if isinstance(hotel, dict):

            safe_hotels.append(
                hotel
            )

    hotels = safe_hotels

    # =========================
    # POLICY FILTERING
    # =========================

    compliant_flights = []

    compliant_hotels = []

    # -------------------------
    # FLIGHT FILTER
    # -------------------------

    for flight in flights:

        if (
            flight.get(
                "travel_class",
                ""
            ).lower()
            == "economy"
        ):

            compliant_flights.append(
                flight
            )

    # -------------------------
    # HOTEL FILTER
    # -------------------------

    for hotel in hotels:

        if (
            hotel.get(
                "price_per_night",
                0
            )
            <= 6000
        ):

            compliant_hotels.append(
                hotel
            )

    # =========================
    # FALLBACKS
    # =========================

    if not compliant_flights:

        compliant_flights = flights

    if not compliant_hotels:

        compliant_hotels = hotels

    # =========================
    # LLM PROMPT
    # =========================

    prompt = OPTIMIZER_PROMPT.format(

        flights=compliant_flights,

        hotels=compliant_hotels,

        policy_results=policy_results
    )

    response = llm.invoke(prompt)

    content = response.content.strip()

    print("\nOPTIMIZER AGENT RAW OUTPUT:\n")

    print(content)

    try:

        # =========================
        # JSON EXTRACTION
        # =========================

        json_match = re.search(
            r'(\{[\s\S]*\})',
            content
        )

        if not json_match:

            raise Exception(
                "No JSON found"
            )

        cleaned = json_match.group(1)

        parsed = json.loads(cleaned)

        selected_flight_id = parsed.get(
            "selected_flight_id"
        )

        selected_hotel_id = parsed.get(
            "selected_hotel_id"
        )

        optimization_reason = parsed.get(
            "reason",
            ""
        )

        # =========================
        # VALID FLIGHT MAP
        # =========================

        valid_flight_map = {

            flight["flight_id"]: flight

            for flight in compliant_flights
        }

        # =========================
        # VALID HOTEL MAP
        # =========================

        valid_hotel_map = {

            hotel["hotel_id"]: hotel

            for hotel in compliant_hotels
        }

        # =========================
        # MATCH FLIGHT
        # =========================

        selected_flight = valid_flight_map.get(
            selected_flight_id
        )

        # deterministic fallback
        if not selected_flight:

            compliant_flights.sort(

                key=lambda x: x.get(
                    "price",
                    999999
                )
            )

            selected_flight = (
                compliant_flights[0]
            )

        # =========================
        # MATCH HOTEL
        # =========================

        selected_hotel = valid_hotel_map.get(
            selected_hotel_id
        )

        # deterministic fallback
        if not selected_hotel:

            compliant_hotels.sort(

                key=lambda x: (
                    -x.get("rating", 0),
                    x.get(
                        "price_per_night",
                        999999
                    )
                )
            )

            selected_hotel = (
                compliant_hotels[0]
            )

        # =========================
        # TOTAL COST
        # =========================

        total_trip_cost = (

            selected_flight.get(
                "price",
                0
            )

            +

            selected_hotel.get(
                "price_per_night",
                0
            )
        )

        # =========================
        # FINAL ITINERARY
        # =========================

        optimized_itinerary = {

            "selected_flight":
            selected_flight,

            "selected_hotel":
            selected_hotel,

            "optimization_reason":
            optimization_reason,

            "total_trip_cost":
            total_trip_cost
        }

        return optimized_itinerary

    except Exception as e:

        print("\nOPTIMIZER AGENT ERROR:\n")

        print(e)

        # =========================
        # SAFE FALLBACKS
        # =========================

        fallback_flight = (

            compliant_flights[0]

            if compliant_flights

            else {}
        )

        fallback_hotel = (

            compliant_hotels[0]

            if compliant_hotels

            else {}
        )

        return {

            "selected_flight":
            fallback_flight,

            "selected_hotel":
            fallback_hotel,

            "optimization_reason":
            "Fallback optimization used.",

            "total_trip_cost":
            (
                fallback_flight.get(
                    "price",
                    0
                )

                +

                fallback_hotel.get(
                    "price_per_night",
                    0
                )
            )
        }