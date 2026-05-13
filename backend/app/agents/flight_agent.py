import json

from app.core.llm import (
    llm
)

from app.db.mock_flight_db import (
    search_flights
)


def flight_agent(

    source,
    destinations,
    preferences
):

    all_selected_flights = []

    current_source = source

    for destination in destinations:

        available_flights = search_flights(

            current_source,
            destination
        )

        if not available_flights:
            current_source = destination
            continue

        prompt = f"""
You are an enterprise travel flight recommendation agent.

TASK:
Select the BEST flight.

RULES:

1. Prefer economy flights
2. Avoid morning flights if requested
3. Prefer fewer stops
4. Prefer cheaper flights
5. Prefer business-friendly timings
6. NEVER hallucinate
7. ONLY use provided flights
8. RETURN STRICT JSON ONLY

OUTPUT FORMAT:

{{
  "selected_flight_id": "",
  "reason": ""
}}

USER PREFERENCES:
{json.dumps(preferences, indent=2)}

AVAILABLE FLIGHTS:
{json.dumps(available_flights, indent=2)}
"""

        try:

            response = llm.invoke(
                prompt
            )

            content = response.content.strip()

            print(
                "\nFLIGHT AGENT RAW OUTPUT:\n"
            )

            print(content)

            if "```json" in content:

                content = content.split(
                    "```json"
                )[1].split(
                    "```"
                )[0]

            result = json.loads(
                content
            )

            selected_id = result.get(
                "selected_flight_id"
            )

            selected_flight = next(

                (
                    flight

                    for flight in available_flights

                    if flight.get(
                        "flight_id"
                    ) == selected_id
                ),

                None
            )

            if selected_flight:

                selected_flight[
                    "reason"
                ] = result.get(
                    "reason",
                    ""
                )

                all_selected_flights.append(
                    selected_flight
                )

        except Exception as e:

            print(
                "\nFLIGHT AGENT ERROR:\n"
            )

            print(str(e))

            fallback_flights = sorted(

                available_flights,

                key=lambda x: (

                    x.get(
                        "travel_class"
                    ) != "economy",

                    x.get(
                        "stops",
                        99
                    ),

                    x.get(
                        "price",
                        999999
                    )
                )
            )

            if fallback_flights:

                fallback = fallback_flights[0]

                fallback[
                    "reason"
                ] = (
                    "Fallback selection used."
                )

                all_selected_flights.append(
                    fallback
                )

        current_source = destination

    return all_selected_flights