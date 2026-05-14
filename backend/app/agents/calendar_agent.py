from datetime import datetime


def calendar_agent(
    meetings,
    flights,
    existing_calendar
):
    schedule_analysis = []
    conflicts = []

    for meeting in meetings or []:
        city = meeting.get("city", "")
        flight = _flight_to_city(
            flights,
            city
        )
        arrival_time = flight.get("arrival_time", "") if flight else ""
        meeting_time = meeting.get("time") or meeting.get("meeting_time") or ""
        buffer_minutes = _buffer_minutes(
            arrival_time,
            meeting_time
        )
        feasible = buffer_minutes >= 90

        schedule_analysis.append(
            {
                "city": city,
                "meeting_date": meeting.get("date") or meeting.get("meeting_date") or "",
                "meeting_time": meeting_time,
                "arrival_time": arrival_time,
                "buffer_minutes": max(0, buffer_minutes),
                "feasible": feasible,
                "risk_level": "low" if feasible else "high",
            }
        )

        if not feasible:
            conflicts.append(
                {
                    "city": city,
                    "reason": "Less than 90 minutes between arrival and meeting.",
                }
            )

    return {
        "schedule_analysis": schedule_analysis,
        "conflicts": conflicts,
    }


def _flight_to_city(
    flights,
    city
):
    for flight in flights or []:
        if str(flight.get("destination", "")).lower() == str(city).lower():
            return flight
    return {}


def _buffer_minutes(
    arrival_time,
    meeting_time
):
    arrival = _parse_time(arrival_time)
    meeting = _parse_time(meeting_time)

    if not arrival or not meeting:
        return 120

    return int(
        (meeting - arrival).total_seconds() / 60
    )


def _parse_time(
    value
):
    value = str(value or "").strip().upper()
    for fmt in ("%I:%M %p", "%I %p"):
        try:
            return datetime.strptime(
                value,
                fmt
            )
        except ValueError:
            continue
    return None
