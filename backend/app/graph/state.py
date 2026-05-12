from typing import TypedDict
from typing import List
from typing import Dict
from typing import Any


class TravelState(TypedDict):

    # =========================
    # USER INPUT
    # =========================

    user_input: str

    employee_id: str


    # =========================
    # EMPLOYEE CONTEXT
    # =========================

    employee_context: Dict[str, Any]


    # =========================
    # PARSED REQUEST
    # =========================

    parsed_request: Dict[str, Any]


    # =========================
    # WORKFLOW EXECUTION
    # =========================

    next_steps: List[str]

    current_step: str

    request_type: str


    # =========================
    # CALENDAR DATA
    # =========================

    calendar_events: List[Dict]

    calendar_conflicts: List[Dict]


    # =========================
    # FLIGHT DATA
    # =========================

    flight_options: List[Dict]


    # =========================
    # HOTEL DATA
    # =========================

    hotel_options: List[Dict]


    # =========================
    # POLICY VALIDATION
    # =========================

    policy_results: Dict[str, Any]


    # =========================
    # FINAL ITINERARY
    # =========================

    optimized_itinerary: Dict[str, Any]


    # =========================
    # FINAL RESPONSE
    # =========================

    final_response: str


    # =========================
    # EXECUTION LOGS
    # =========================

    execution_logs: List[str]