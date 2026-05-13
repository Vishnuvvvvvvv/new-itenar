import json

from app.core.llm import (
    llm
)


APPROVAL_PROMPT = """
You are an enterprise travel approval agent.

Your task is to determine whether
a business trip requires approval.

Consider:
1. total trip cost
2. policy violations
3. business class usage
4. luxury hotel usage
5. compliance status
6. risk level

Trip Cost:
{trip_cost}

Policy Results:
{policy_results}

Selected Flight:
{selected_flight}

Selected Hotel:
{selected_hotel}

Return ONLY valid JSON.

Example:

{{
    "approval_required": true,
    "approval_level": "Manager",
    "reason": "Trip exceeds allowed budget"
}}
"""


def approval_agent(

    optimized_itinerary,

    policy_results
):

    selected_flight = (
        optimized_itinerary.get(
            "selected_flight",
            {}
        )
    )

    selected_hotel = (
        optimized_itinerary.get(
            "selected_hotel",
            {}
        )
    )

    total_trip_cost = (
        optimized_itinerary.get(
            "total_trip_cost",
            0
        )
    )

    prompt = (
        APPROVAL_PROMPT.format(

            trip_cost=total_trip_cost,

            policy_results=json.dumps(
                policy_results,
                indent=2
            ),

            selected_flight=json.dumps(
                selected_flight,
                indent=2
            ),

            selected_hotel=json.dumps(
                selected_hotel,
                indent=2
            )
        )
    )

    response = llm.invoke(
        prompt
    )

    raw_output = (
        response.content.strip()
    )

    print(
        "\nAPPROVAL AGENT RAW OUTPUT:\n"
    )

    print(raw_output)

    try:

        parsed = json.loads(
            raw_output
        )

        return parsed

    except Exception as e:

        print(
            "\nAPPROVAL AGENT ERROR:\n"
        )

        print(str(e))

        return {

            "approval_required": True,

            "approval_level": "Manager",

            "reason":
            "Fallback approval used."
        }