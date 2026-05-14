import os
import re

from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


CITY_ALIASES = [
    "Chennai",
    "Bangalore",
    "Bengaluru",
    "Hyderabad",
    "Mumbai",
    "Delhi",
]


def parser_agent(
    user_input
):
    if os.getenv("ENABLE_LLM_AGENTS", "false").lower() != "true":
        return fallback_parse(user_input)

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

        if not parsed:
            return fallback_parse(user_input)

        return parsed

    except Exception as e:

        print(
            "\nPARSER ERROR:\n"
        )

        print(str(e))

        return fallback_parse(user_input)


def fallback_parse(user_input):
    text = user_input or ""
    lower_text = text.lower()
    city_matches = []

    for city in CITY_ALIASES:
        for match in re.finditer(
            city.lower(),
            lower_text
        ):
            normalized = "Bangalore" if city == "Bengaluru" else city
            city_matches.append(
                (
                    match.start(),
                    normalized
                )
            )

    cities = []
    for _, city in sorted(city_matches):
        if city not in cities:
            cities.append(city)

    source = ""
    destinations = cities
    source_match = re.search(
        r"from\s+([a-zA-Z]+)",
        lower_text
    )
    if source_match:
        raw_source = source_match.group(1).lower()
        for city in CITY_ALIASES:
            if city.lower() == raw_source:
                source = "Bangalore" if city == "Bengaluru" else city
                break

    if source:
        destinations = [
            city for city in cities
            if city.lower() != source.lower()
        ]
    elif len(cities) > 1:
        source = cities[0]
        destinations = cities[1:]

    preferences = []
    if "avoid morning" in lower_text or "no morning" in lower_text:
        preferences.append("avoid morning flights")
    if "business hotel" in lower_text:
        preferences.append("prefer business hotels")
    if "cab" in lower_text:
        preferences.append("prefer cabs")
    if "taxi" in lower_text:
        preferences.append("prefer taxi")
    if "metro" in lower_text:
        preferences.append("prefer metro")

    dates = re.findall(
        r"\d{4}-\d{2}-\d{2}",
        text
    )

    return {
        "source": source,
        "destinations": destinations,
        "start_date": dates[0] if dates else "",
        "end_date": dates[1] if len(dates) > 1 else "",
        "purpose": "Business travel",
        "meetings": [],
        "preferences": preferences,
    }
