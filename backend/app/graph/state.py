from typing import (
    TypedDict,
    List,
    Dict,
    Any
)


class TravelState(
    TypedDict
):

    user_input: str

    employee_id: str

    parsed_request: Dict[str, Any]

    request_type: str

    next_steps: List[str]

    employee_context: Dict[str, Any]

    calendar_events: List[Dict[str, Any]]

    calendar_conflicts: List[Dict[str, Any]]

    schedule_analysis: List[Dict[str, Any]]

    flight_options: List[Dict[str, Any]]

    hotel_options: List[Dict[str, Any]]

    transport_options: List[Dict[str, Any]]

    optimized_itinerary: Dict[str, Any]

    policy_results: Dict[str, Any]

    approval_workflow: Dict[str, Any]

    final_response: str

    execution_logs: List[str]