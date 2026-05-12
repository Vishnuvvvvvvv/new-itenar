import json
import re

from app.core.llm import llm


SUPERVISOR_PROMPT = """
You are an enterprise AI workflow orchestration agent.

Your task is to classify the user request
and decide which agents should execute.

Available agents:
- calendar
- flight
- hotel
- policy
- optimizer
- explanation
- booking
- export

IMPORTANT RULES:

1. Calendar conflict / schedule / meeting queries
MUST use:
calendar, explanation

2. Travel planning requests
MUST use:
calendar, flight, hotel,
policy, optimizer, explanation

3. Export requests
MUST use:
export

4. Booking requests
MUST use:
booking

5. Return ONLY valid JSON.

========================
EXAMPLES
========================

USER:
"Show my travel conflicts next week"

OUTPUT:
{{
    "request_type": "calendar_analysis",
    "next_steps": [
        "calendar",
        "explanation"
    ]
}}

USER:
"Plan a Bangalore business trip"

OUTPUT:
{{
    "request_type": "travel_planning",
    "next_steps": [
        "calendar",
        "flight",
        "hotel",
        "policy",
        "optimizer",
        "explanation"
    ]
}}

USER:
"Export my itinerary"

OUTPUT:
{{
    "request_type": "export",
    "next_steps": [
        "export"
    ]
}}

USER:
"Book my finalized itinerary"

OUTPUT:
{{
    "request_type": "booking",
    "next_steps": [
        "booking"
    ]
}}

========================

Parsed Request:
{parsed_request}

User Input:
{user_input}

Return ONLY JSON.
"""


def supervisor_agent(
    parsed_request,
    user_input
):

    prompt = SUPERVISOR_PROMPT.format(
        parsed_request=parsed_request,
        user_input=user_input
    )

    response = llm.invoke(prompt)

    content = response.content

    print("\nSUPERVISOR RAW OUTPUT:\n")
    print(content)

    try:

        # Extract ONLY JSON
        json_match = re.search(
            r'\{[\s\S]*\}',
            content
        )

        if json_match:

            cleaned = json_match.group()

            parsed_data = json.loads(cleaned)

            return parsed_data

        raise ValueError(
            "No JSON found"
        )

    except Exception as e:

        print("\nSUPERVISOR JSON ERROR:\n")
        print(e)

        return {
            "request_type": "travel_planning",
            "next_steps": [
                "calendar",
                "flight",
                "hotel",
                "policy",
                "optimizer",
                "explanation"
            ]
        }