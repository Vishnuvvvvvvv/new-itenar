import json

from app.core.llm import (
    llm
)

from app.db.hotel_db import (
    search_hotels
)

from app.utils.json_parser import (
    extract_json
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

        prompt = f"""
You are an enterprise hotel recommendation agent.

TASK:
Select the BEST hotel.

RULES:

1. Prefer business hotels
2. Prefer office proximity
3. Prefer good ratings
4. Prefer reasonable pricing
5. Return STRICT JSON ONLY
6. NEVER explain outside JSON
7. NEVER generate code
8. NEVER hallucinate hotels

FORMAT:

{{
  "selected_hotel_id": "",
  "reason": ""
}}

USER PREFERENCES:
{json.dumps(preferences, indent=2)}

AVAILABLE HOTELS:
{json.dumps(available_hotels, indent=2)}
"""

        try:

            response = llm.invoke(
                prompt
            )

            content = response.content.strip()

            print(
                "\nHOTEL AGENT RAW OUTPUT:\n"
            )

            print(content)

            result = extract_json(
                content
            )

            selected_id = result.get(
                "selected_hotel_id"
            )

            selected_hotel = next(

                (
                    hotel

                    for hotel in available_hotels

                    if hotel.get(
                        "hotel_id"
                    ) == selected_id
                ),

                None
            )

            if selected_hotel:

                selected_hotel[
                    "reason"
                ] = result.get(
                    "reason",
                    ""
                )

                selected_hotels.append(
                    selected_hotel
                )

        except Exception as e:

            print(
                "\nHOTEL AGENT ERROR:\n"
            )

            print(str(e))

    return selected_hotels