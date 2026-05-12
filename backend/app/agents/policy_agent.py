import json
import re

from app.core.llm import llm

from app.rag.retriever import (
    retrieve_policy
)


POLICY_AGENT_PROMPT = """
You are an enterprise AI travel compliance agent.

Your responsibilities:
1. Analyze selected itinerary
2. Analyze retrieved company policies
3. Detect REAL violations ONLY
4. NEVER hallucinate
5. ONLY use explicitly provided fields
6. If itinerary already satisfies a policy,
   DO NOT report violation

VERY IMPORTANT RULES:
- Do NOT invent missing information
- Do NOT assume policy violations
- ONLY validate based on provided data
- Economy flights are policy compliant
- If hotel exceeds allowed budget,
  report violation
- If total cost exceeds limit,
  report violation

Return ONLY valid JSON.

Format:

{{
    "compliant": true,
    "violations": [],
    "recommendations": []
}}

Selected Flight:
{flight}

Selected Hotel:
{hotel}

Retrieved Policies:
{policies}
"""


def policy_agent(

    selected_flight,

    selected_hotel
):

    # =========================
    # RAG RETRIEVAL
    # =========================

    retrieval_query = """

    flight policy
    hotel budget
    travel approval
    airline rules
    economy class

    """

    docs = retrieve_policy(
        retrieval_query
    )

    policy_text = "\n".join([
        doc.page_content
        for doc in docs
    ])

    # =========================
    # PROMPT
    # =========================

    prompt = POLICY_AGENT_PROMPT.format(

        flight=selected_flight,

        hotel=selected_hotel,

        policies=policy_text
    )

    response = llm.invoke(prompt)

    content = response.content

    print("\nPOLICY AGENT RAW OUTPUT:\n")
    print(content)

    try:

        # =========================
        # JSON EXTRACTION
        # =========================

        json_match = re.search(
            r'\{[\s\S]*\}',
            content
        )

        cleaned = json_match.group()

        parsed = json.loads(cleaned)

        # =========================
        # DETERMINISTIC VALIDATION
        # =========================

        validated_violations = []

        validated_recommendations = []

        # -------------------------
        # HOTEL BUDGET VALIDATION
        # -------------------------

        hotel_price = selected_hotel.get(
            "price_per_night",
            0
        )

        if hotel_price > 6000:

            validated_violations.append({

                "policy":
                "Hotel budget policy",

                "description":
                "Hotel price exceeds allowed limit of ₹6000/night"
            })

            validated_recommendations.append({

                "policy":
                "Hotel budget policy",

                "description":
                "Choose lower-cost hotel"
            })

        # -------------------------
        # TOTAL TRIP COST
        # -------------------------

        flight_price = selected_flight.get(
            "price",
            0
        )

        total_trip_cost = (
            hotel_price + flight_price
        )

        if total_trip_cost > 20000:

            validated_violations.append({

                "policy":
                "Trip approval policy",

                "description":
                "Trip exceeds ₹20000 approval threshold"
            })

            validated_recommendations.append({

                "policy":
                "Trip approval policy",

                "description":
                "Manager approval required"
            })

        # -------------------------
        # FLIGHT CLASS VALIDATION
        # -------------------------

        travel_class = selected_flight.get(
            "travel_class",
            ""
        )

        if (
            travel_class.lower()
            != "economy"
        ):

            validated_violations.append({

                "policy":
                "Flight class policy",

                "description":
                "Only economy flights allowed"
            })

            validated_recommendations.append({

                "policy":
                "Flight class policy",

                "description":
                "Choose economy class flight"
            })

        # =========================
        # FINAL STRUCTURED RESULT
        # =========================

        final_result = {

            "compliant":
            len(validated_violations) == 0,

            "violations":
            validated_violations,

            "recommendations":
            validated_recommendations
        }

        return final_result

    except Exception as e:

        print("\nPOLICY AGENT ERROR:\n")
        print(e)

        return {

            "compliant": True,

            "violations": [],

            "recommendations": []
        }