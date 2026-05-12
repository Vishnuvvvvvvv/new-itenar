from app.utils.json_loader import (
    load_json_file
)


EMPLOYEE_FILE = (
    "app/mock_server/employees.json"
)


def get_employee(employee_id):

    employees = load_json_file(
        EMPLOYEE_FILE
    )

    for employee in employees:

        if (
            employee["employee_id"]
            == employee_id
        ):

            return employee

    return None