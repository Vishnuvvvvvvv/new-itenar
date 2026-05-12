from pydantic import BaseModel

from typing import List, Dict, Any


class TravelRequest(BaseModel):

    user_input: str

    employee_id: str


class TravelResponse(BaseModel):

    final_response: str

    request_type: str

    employee_context: Dict[str, Any]

    flight_options: List[Dict[str, Any]]

    hotel_options: List[Dict[str, Any]]

    policy_results: Dict[str, Any]

    optimized_itinerary: Dict[str, Any]

    execution_logs: List[str]