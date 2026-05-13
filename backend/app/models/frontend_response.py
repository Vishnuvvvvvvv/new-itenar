from pydantic import BaseModel
from typing import List, Dict, Any


class FrontendTravelResponse(
    BaseModel
):

    chat_summary: str

    itinerary: Dict[str, Any]

    flights: List[Dict[str, Any]]

    hotels: List[Dict[str, Any]]

    transports: List[Dict[str, Any]]

    policy: Dict[str, Any]

    approval: Dict[str, Any]

    calendar_analysis: Dict[str, Any]

    execution_logs: List[str]