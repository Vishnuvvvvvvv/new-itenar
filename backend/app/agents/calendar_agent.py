import json

from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


def calendar_agent(

    meetings,
    flights,
    existing_calendar
):

    prompt = f"""
You are an enterprise calendar intelligence agent.

TASK:

Analyze:

1. Meeting feasibility
2. Flight arrival feasibility
3. Schedule overlaps
4. Existing employee calendar conflicts
5. Risky schedules
6. Business practicality

RULES:

- Minimum safe buffer:
  90 minutes before meetings

- Detect:
  - overlapping meetings
  - impossible travel
  - insufficient commute buffers
  - overloaded schedules

IMPORTANT:
- Return STRICT JSON ONLY
- DO NOT explain
- DO NOT generate markdown
- DO NOT generate code

OUTPUT FORMAT:

{{
  "schedule_analysis": [
    {{
      "city": "",
      "meeting_date": "",
      "meeting_time": "",
      "arrival_time": "",
      "buffer_minutes": 0,
      "feasible": true,
      "risk_level": ""
    }}
  ],
  "conflicts": []
}}

=========================
NEW TRAVEL MEETINGS
=========================

{json.dumps(meetings, indent=2)}

=========================
AVAILABLE FLIGHTS
=========================

{json.dumps(flights, indent=2)}

=========================
EXISTING EMPLOYEE CALENDAR
=========================

{json.dumps(existing_calendar, indent=2)}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nCALENDAR AGENT RAW OUTPUT:\n"
        )

        print(content)

        result = extract_json(
            content
        )

        return result

    except Exception as e:

        print(
            "\nCALENDAR AGENT ERROR:\n"
        )

        print(str(e))

        return {

            "schedule_analysis": [],

            "conflicts": [
                "Fallback calendar analysis used."
            ]
        }
import json

from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


def calendar_agent(

    meetings,
    flights,
    existing_calendar
):

    prompt = f"""
You are an enterprise calendar intelligence agent.

TASK:

Analyze:

1. Meeting feasibility
2. Flight arrival feasibility
3. Schedule overlaps
4. Existing employee calendar conflicts
5. Risky schedules
6. Business practicality

RULES:

- Minimum safe buffer:
  90 minutes before meetings

- Detect:
  - overlapping meetings
  - impossible travel
  - insufficient commute buffers
  - overloaded schedules

IMPORTANT:
- Return STRICT JSON ONLY
- DO NOT explain
- DO NOT generate markdown
- DO NOT generate code

OUTPUT FORMAT:

{{
  "schedule_analysis": [
    {{
      "city": "",
      "meeting_date": "",
      "meeting_time": "",
      "arrival_time": "",
      "buffer_minutes": 0,
      "feasible": true,
      "risk_level": ""
    }}
  ],
  "conflicts": []
}}

=========================
NEW TRAVEL MEETINGS
=========================

{json.dumps(meetings, indent=2)}

=========================
AVAILABLE FLIGHTS
=========================

{json.dumps(flights, indent=2)}

=========================
EXISTING EMPLOYEE CALENDAR
=========================

{json.dumps(existing_calendar, indent=2)}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nCALENDAR AGENT RAW OUTPUT:\n"
        )

        print(content)

        result = extract_json(
            content
        )

        return result

    except Exception as e:

        print(
            "\nCALENDAR AGENT ERROR:\n"
        )

        print(str(e))

        return {

            "schedule_analysis": [],

            "conflicts": [
                "Fallback calendar analysis used."
            ]
        }
import json

from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


def calendar_agent(

    meetings,
    flights,
    existing_calendar
):

    prompt = f"""
You are an enterprise calendar intelligence agent.

TASK:

Analyze:

1. Meeting feasibility
2. Flight arrival feasibility
3. Schedule overlaps
4. Existing employee calendar conflicts
5. Risky schedules
6. Business practicality

RULES:

- Minimum safe buffer:
  90 minutes before meetings

- Detect:
  - overlapping meetings
  - impossible travel
  - insufficient commute buffers
  - overloaded schedules

IMPORTANT:
- Return STRICT JSON ONLY
- DO NOT explain
- DO NOT generate markdown
- DO NOT generate code

OUTPUT FORMAT:

{{
  "schedule_analysis": [
    {{
      "city": "",
      "meeting_date": "",
      "meeting_time": "",
      "arrival_time": "",
      "buffer_minutes": 0,
      "feasible": true,
      "risk_level": ""
    }}
  ],
  "conflicts": []
}}

=========================
NEW TRAVEL MEETINGS
=========================

{json.dumps(meetings, indent=2)}

=========================
AVAILABLE FLIGHTS
=========================

{json.dumps(flights, indent=2)}

=========================
EXISTING EMPLOYEE CALENDAR
=========================

{json.dumps(existing_calendar, indent=2)}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nCALENDAR AGENT RAW OUTPUT:\n"
        )

        print(content)

        result = extract_json(
            content
        )

        return result

    except Exception as e:

        print(
            "\nCALENDAR AGENT ERROR:\n"
        )

        print(str(e))

        return {

            "schedule_analysis": [],

            "conflicts": [
                "Fallback calendar analysis used."
            ]
        }
import json

from app.core.llm import (
    llm
)

from app.utils.json_parser import (
    extract_json
)


def calendar_agent(

    meetings,
    flights,
    existing_calendar
):

    prompt = f"""
You are an enterprise calendar intelligence agent.

TASK:

Analyze:

1. Meeting feasibility
2. Flight arrival feasibility
3. Schedule overlaps
4. Existing employee calendar conflicts
5. Risky schedules
6. Business practicality

RULES:

- Minimum safe buffer:
  90 minutes before meetings

- Detect:
  - overlapping meetings
  - impossible travel
  - insufficient commute buffers
  - overloaded schedules

IMPORTANT:
- Return STRICT JSON ONLY
- DO NOT explain
- DO NOT generate markdown
- DO NOT generate code

OUTPUT FORMAT:

{{
  "schedule_analysis": [
    {{
      "city": "",
      "meeting_date": "",
      "meeting_time": "",
      "arrival_time": "",
      "buffer_minutes": 0,
      "feasible": true,
      "risk_level": ""
    }}
  ],
  "conflicts": []
}}

=========================
NEW TRAVEL MEETINGS
=========================

{json.dumps(meetings, indent=2)}

=========================
AVAILABLE FLIGHTS
=========================

{json.dumps(flights, indent=2)}

=========================
EXISTING EMPLOYEE CALENDAR
=========================

{json.dumps(existing_calendar, indent=2)}
"""

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content.strip()

        print(
            "\nCALENDAR AGENT RAW OUTPUT:\n"
        )

        print(content)

        result = extract_json(
            content
        )

        return result

    except Exception as e:

        print(
            "\nCALENDAR AGENT ERROR:\n"
        )

        print(str(e))

        return {

            "schedule_analysis": [],

            "conflicts": [
                "Fallback calendar analysis used."
            ]
        }