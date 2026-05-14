from fastapi import APIRouter

from app.services.travel_service import (
    TravelPlannerService
)
from app.services.session_service import (
    session_service
)

from app.models.frontend_request import (
    FrontendTripRequest
)

router = APIRouter()

service = TravelPlannerService()

@router.post(
    "/frontend-plan-trip"
)
async def frontend_plan_trip(
    request: FrontendTripRequest
):
    login_result = session_service.login(
        request.employee_id,
        "demo"
    )

    result = session_service.chat(
        login_result["session_id"],
        request.user_input
    )

    return {

        "chat_summary":
        result.get("assistant_message"),

        "itinerary":
        result.get(
            "itinerary"
        ),

        "itinerary_days":
        result.get(
            "itinerary_days",
            []
        ),

        "rankings":
        result.get(
            "rankings",
            {}
        ),

        "flights":
        result.get(
            "flights",
            []
        ),

        "hotels":
        result.get(
            "hotels",
            []
        ),

        "transports":
        result.get(
            "transports",
            []
        ),

        "policy":
        result.get(
            "policy",
            {}
        ),

        "approval":
        result.get(
            "approval",
            {}
        ),

        "booking_state":
        result.get(
            "booking_state",
            {}
        ),

        "calendar_analysis":
        result.get(
            "calendar_analysis",
            {}
        ),

        "execution_logs":
        result.get(
            "execution_logs",
            []
        )
    }
