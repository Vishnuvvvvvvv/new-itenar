import json
import re

from app.core.llm import llm

from app.mcp_tools.hotel_tool import (
    search_hotels
)
HOTEL_AGENT_PROMPT = """
You are an enterprise AI hotel recommendation agent.

Analyze:
- user preferences
- hotel options

Recommend the BEST hotels.

IMPORTANT:
- Return ONLY valid JSON
- Do NOT explain anything
- Do NOT generate Python code
- Do NOT generate markdown
- Do NOT generate headings
- Output MUST start with {{
- Output MUST end with }}

Required format:

{{
    "recommended_hotels": [
        {{
            "hotel_id": "",
            "reason": ""
        }}
    ]
}}

User Preferences:
{preferences}

Available Hotels:
{hotels}
"""


def hotel_agent(parsed_request):

    destination = parsed_request.get(
        "destination"
    )

    preferences = parsed_request.get(
        "preferences",
        []
    )

    hotels = search_hotels(
        destination
    )

    prompt = HOTEL_AGENT_PROMPT.format(
        preferences=preferences,
        hotels=hotels
    )

    response = llm.invoke(prompt)

    content = response.content

    print("\nHOTEL AGENT RAW OUTPUT:\n")
    print(content)

    try:

        json_match = re.search(
    r'```json\s*(\{[\s\S]*?\})\s*```',
    content
)

        if json_match:

            cleaned = json_match.group(1)

        else:

            fallback_match = re.search(
                r'(\{[\s\S]*\})',
                content
            )

            cleaned = fallback_match.group(1)

        parsed = json.loads(cleaned)

        recommendations = parsed[
            "recommended_hotels"
        ]

        final_hotels = []

        for rec in recommendations:

            for hotel in hotels:

                if (
                    hotel["hotel_id"]
                    == rec["hotel_id"]
                ):

                    hotel["reason"] = rec[
                        "reason"
                    ]

                    final_hotels.append(
                        hotel
                    )

        return final_hotels

    except Exception as e:

        print("\nHOTEL AGENT ERROR:\n")
        print(e)

        return hotels