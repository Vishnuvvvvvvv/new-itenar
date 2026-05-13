import json

from app.core.llm import (
    llm
)

from app.db.mock_transport_db import (
    get_transport_options
)

from app.utils.json_parser import (
    extract_json
)


def transport_agent(
    cities
):

    selected_transports = []

    for city in cities:

        transport_options = (
            get_transport_options(
                city
            )
        )

        if not transport_options:
            continue

        prompt = f"""
You are an enterprise local transport recommendation agent.

TASK:
Select the BEST transport option.

Prioritize:
- business convenience
- office proximity
- commute efficiency
- comfort
- reasonable pricing

IMPORTANT:
- Return STRICT JSON ONLY
- DO NOT explain
- DO NOT generate markdown
- DO NOT generate code

OUTPUT FORMAT:

{{
  "selected_transport_id": "",
  "reason": ""
}}

=========================
CITY
=========================

{city}

=========================
AVAILABLE TRANSPORT OPTIONS
=========================

{json.dumps(transport_options, indent=2)}
"""

        try:

            response = llm.invoke(
                prompt
            )

            content = response.content.strip()

            print(
                "\nTRANSPORT AGENT RAW OUTPUT:\n"
            )

            print(content)

            result = extract_json(
                content
            )

            selected_id = result.get(
                "selected_transport_id"
            )

            selected_transport = next(

                (
                    transport

                    for transport
                    in transport_options

                    if transport.get(
                        "transport_id"
                    ) == selected_id
                ),

                None
            )

            if selected_transport:

                selected_transport[
                    "reason"
                ] = result.get(
                    "reason",
                    ""
                )

                selected_transports.append(
                    selected_transport
                )

        except Exception as e:

            print(
                "\nTRANSPORT AGENT ERROR:\n"
            )

            print(str(e))

    return selected_transports