from typing import Any, Dict, List, Optional


def rank_recommendations(
    flights: List[Dict[str, Any]],
    hotels: List[Dict[str, Any]],
    transports: List[Dict[str, Any]],
    preferences: List[Any],
    policy_results: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    preference_text = " ".join(str(item).lower() for item in preferences or [])
    return {
        "flights": _rank(flights, lambda item: _flight_score(item, preference_text)),
        "hotels": _rank(hotels, lambda item: _hotel_score(item, preference_text)),
        "transports": _rank(transports, lambda item: _transport_score(item, preference_text)),
        "policy_context": {
            "compliant": (policy_results or {}).get("compliant", True),
        },
    }


def _rank(items, scorer):
    ranked = []
    for item in items or []:
        score, reason = scorer(item)
        ranked.append(
            {
                **item,
                "ranking_score": max(0, min(100, int(score))),
                "ranking_reason": reason,
            }
        )
    return sorted(ranked, key=lambda option: option.get("ranking_score", 0), reverse=True)


def _flight_score(flight, preference_text):
    score = 72
    reasons = []

    if flight.get("travel_class", "").lower() == "economy":
        score += 10
        reasons.append("economy class")
    else:
        score -= 12
        reasons.append("business class may need approval")

    stops = int(flight.get("stops", 0) or 0)
    score += max(0, 8 - (stops * 6))
    if stops == 0:
        reasons.append("non-stop")

    price = int(flight.get("price", 0) or 0)
    if price <= 5000:
        score += 8
        reasons.append("cost efficient")
    elif price >= 7000:
        score -= 8

    departure = str(flight.get("departure_time", "")).lower()
    if "avoid morning" in preference_text and "am" in departure:
        hour = _extract_hour(departure)
        if hour and hour < 12:
            score -= 15
            reasons.append("morning departure conflicts with preference")
    elif "pm" in departure:
        score += 4
        reasons.append("business-friendly timing")

    return score, ", ".join(reasons) or "balanced cost and convenience"


def _hotel_score(hotel, preference_text):
    score = 68
    reasons = []

    if hotel.get("hotel_type", "").lower() == "business":
        score += 12
        reasons.append("business hotel")
    elif hotel.get("hotel_type", "").lower() == "luxury":
        score -= 10
        reasons.append("luxury category may require approval")

    rating = float(hotel.get("rating", 0) or 0)
    score += int((rating - 3.5) * 8)
    if rating >= 4.4:
        reasons.append("strong rating")

    price = int(hotel.get("price_per_night", 0) or 0)
    if price <= 6000:
        score += 10
        reasons.append("within preferred nightly cost")
    elif price >= 10000:
        score -= 15

    area = str(hotel.get("location_area", "")).lower()
    if any(token in area for token in ["bkc", "electronic", "hitech", "gachibowli", "whitefield"]):
        score += 6
        reasons.append("near common office area")

    return score, ", ".join(reasons) or "balanced hotel option"


def _transport_score(transport, preference_text):
    score = 70
    reasons = []
    transport_type = str(transport.get("transport_type", "")).lower()

    if "cab" in preference_text or "taxi" in preference_text:
        if transport_type in {"cab", "taxi"}:
            score += 12
            reasons.append("matches requested private transport")
        else:
            score -= 6

    if transport.get("comfort_level", "").lower() == "high":
        score += 10
        reasons.append("high comfort")

    cost = int(transport.get("estimated_cost", 0) or 0)
    if cost <= 200:
        score += 8
        reasons.append("low cost")
    elif cost > 400:
        score -= 4

    return score, ", ".join(reasons) or "balanced commute option"


def _extract_hour(value):
    try:
        return int(value.split(":")[0])
    except Exception:
        return None
