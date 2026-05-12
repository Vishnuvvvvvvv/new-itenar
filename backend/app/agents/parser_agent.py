import json
import re

from app.core.llm import llm


PARSER_PROMPT = """
You are an enterprise AI travel planning assistant.

Extract travel information from the user request.

Return ONLY valid JSON.

Required JSON format:

{{
    "destination": "",
    "date": "",
    "purpose": "",
    "preferences": []
}}

User Request:
{user_input}
"""


def parser_agent(user_input: str):

    prompt = PARSER_PROMPT.format(
        user_input=user_input
    )

    response = llm.invoke(prompt)

    content = response.content

    print("\nRAW LLM OUTPUT:\n")
    print(content)

    try:

        # Extract ONLY JSON block
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

        print("\nJSON PARSE ERROR:\n")
        print(e)

        return {
            "destination": "",
            "date": "",
            "purpose": "",
            "preferences": []
        }