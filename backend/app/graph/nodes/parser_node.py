from app.graph.state import TravelState
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.parser_agent import (
    parser_agent,
    fallback_parse
)


CITY_ALIASES = [
    "Chennai",
    "Bangalore",
    "Bengaluru",
    "Hyderabad",
    "Mumbai",
    "Delhi",
]


def parser_node(state: TravelState):
    run_agent_step(
        state,
        "Parser Agent",
        "Extracting source, destinations, dates, purpose, meetings, and preferences."
    )

    user_input = state["user_input"]

    previous_request = state.get(
        "previous_request",
        {}
    ) or {}

    parsed_request = parser_agent(
        user_input
    )

    if previous_request:
        parsed_request = merge_with_previous_request(
            previous_request,
            parsed_request,
            user_input
        )

    state["parsed_request"] = parsed_request

    run_agent_step(
        state,
        "Parser Agent",
        "Structured travel request prepared."
    )

    return state


def merge_with_previous_request(
    previous_request,
    parsed_request,
    user_input
):
    text = (user_input or "").lower()
    is_removal = any(token in text for token in ["avoid ", "remove ", "skip "])

    parsed_values = {
        key: value
        for key, value in (parsed_request or {}).items()
        if value not in ("", [], {}, None)
    }

    if is_removal:
        parsed_values.pop("source", None)
        parsed_values.pop("destinations", None)

    merged = {
        **previous_request,
        **parsed_values,
    }

    destinations = list(merged.get("destinations", []) or [])
    preferences = list(merged.get("preferences", []) or [])

    if is_removal:
        for city in CITY_ALIASES:
            normalized = "Bangalore" if city == "Bengaluru" else city
            if city.lower() in text:
                destinations = [
                    item for item in destinations
                    if item.lower() != normalized.lower()
                ]

    if any(token in text for token in ["add ", "include ", "via "]):
        parsed_fallback = fallback_parse(user_input)
        for city in parsed_fallback.get("destinations", []):
            if city not in destinations and city != merged.get("source"):
                destinations.append(city)

    if "evening" in text:
        preferences.append("prefer evening flights")
    if "avoid morning" in text or "no morning" in text:
        preferences.append("avoid morning flights")
    if "cab" in text:
        preferences.append("prefer cabs")
    if "taxi" in text:
        preferences.append("prefer taxi")
    if "metro" in text:
        preferences.append("prefer metro")

    merged["destinations"] = destinations
    merged["preferences"] = list(dict.fromkeys(preferences))
    return merged
