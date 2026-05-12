import json
import re

from app.core.llm import llm


FLIGHT_AGENT_PROMPT = """
You are an enterprise AI flight recommendation agent.

IMPORTANT:
- Use ONLY provided flight IDs
- Do NOT invent IDs
- Return ONLY valid JSON
- No markdown
- No explanations
- No Python code

Format:

{{
    "recommended_flights": [
        {{
            "flight_id": "",
            "reason": ""
        }}
    ]
}}

Available Flights:
{flights}

User Preferences:
{preferences}
"""


def flight_agent(

    preferences,

    flights,

    employee_context=None
):

    prompt = FLIGHT_AGENT_PROMPT.format(

        preferences=preferences,

        flights=flights
    )

    response = llm.invoke(prompt)

    content = response.content.strip()

    print("\nFLIGHT AGENT RAW OUTPUT:\n")

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

            return flights

        cleaned = json_match.group(1)

        parsed = json.loads(cleaned)

        recommended = parsed.get(
            "recommended_flights",
            []
        )

        # ensure list
        if not isinstance(
            recommended,
            list
        ):

            return flights

        final_flights = []

        valid_flight_map = {

            flight["flight_id"]: flight

            for flight in flights

            if isinstance(flight, dict)
        }

        # =========================
        # SAFE MATCHING
        # =========================

        for item in recommended:

            if not isinstance(
                item,
                dict
            ):

                continue

            flight_id = item.get(
                "flight_id"
            )

            reason = item.get(
                "reason",
                ""
            )

            if (
                flight_id
                in valid_flight_map
            ):

                matched_flight = dict(

                    valid_flight_map[
                        flight_id
                    ]
                )

                matched_flight[
                    "reason"
                ] = reason

                final_flights.append(
                    matched_flight
                )

        # =========================
        # SAFE FALLBACK
        # =========================

        if not final_flights:

            return flights

        return final_flights

    except Exception as e:

        print("\nFLIGHT AGENT ERROR:\n")

        print(e)

        return flights