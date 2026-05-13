from app.utils.json_loader import (
    load_json_file
)

CALENDAR_FILE = (
    "app/mock_server/calendar_events.json"
)


def get_employee_calendar(
    employee_id
):

    events = load_json_file(
        CALENDAR_FILE
    )

    employee_events = []

    for event in events:

        if (
            event["employee_id"]
            ==
            employee_id
        ):

            employee_events.append(
                event
            )

    return employee_events