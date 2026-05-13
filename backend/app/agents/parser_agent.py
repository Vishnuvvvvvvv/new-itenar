from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


def parser_agent(
    user_input
):

    prompt = f"""
You are an enterprise travel parser agent.

Extract structured travel planning information.

IMPORTANT:
- Return STRICT JSON ONLY
- DO NOT explain
- DO NOT generate markdown
- DO NOT generate code

OUTPUT FORMAT:

{{
  "source": "",
  "destinations": [],
  "start_date": "",
  "end_date": "",
  "purpose": "",
  "meetings": [
    {{
      "city": "",
      "date": "",
      "time": "",
      "location": ""
    }}
  ],
  "preferences": []
}}

USER INPUT:
{user_input}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nRAW LLM OUTPUT:\n"
        )

        print(content)

        parsed = extract_json(
            content
        )

        return parsed

    except Exception as e:

        print(
            "\nPARSER ERROR:\n"
        )

        print(str(e))

        return {}