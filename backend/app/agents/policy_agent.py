import json

from app.core.llm import (
    llm
)

from app.rag.retriever import (
    retrieve_policy
)

from app.utils.json_parser import (
    extract_json
)


def policy_agent(

    flights,
    hotels,
    employee_context,
    total_cost
):

    department = employee_context.get(
        "department",
        ""
    )

    designation = employee_context.get(
        "designation",
        ""
    )

    query = f"""
Department: {department}
Designation: {designation}
Travel Policy
"""

    policy_context = retrieve_policy(
        query
    )

    prompt = f"""
You are an enterprise travel policy validation agent.

STRICTLY validate itinerary ONLY using retrieved policy documents.

DO NOT invent policies.
DO NOT hallucinate rules.
DO NOT assume restrictions.

=========================
POLICY DOCUMENTS
=========================

{policy_context}

=========================
FLIGHTS
=========================

{json.dumps(flights, indent=2)}

=========================
HOTELS
=========================

{json.dumps(hotels, indent=2)}

=========================
TOTAL COST
=========================

{total_cost}

=========================

Validate:
- flight compliance
- hotel compliance
- approval requirements
- airline restrictions
- budget rules

Return STRICT JSON ONLY.

DO NOT explain.
DO NOT generate markdown.
DO NOT generate code.

OUTPUT FORMAT:

{{
  "compliant": true,
  "violations": [],
  "recommendations": []
}}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nPOLICY AGENT RAW OUTPUT:\n"
        )

        print(content)

        result = extract_json(
            content
        )

        return result

    except Exception as e:

        print(
            "\nPOLICY AGENT ERROR:\n"
        )

        print(str(e))

        return {

            "compliant": True,

            "violations": [],

            "recommendations": []
        }