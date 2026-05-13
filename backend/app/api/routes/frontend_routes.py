from fastapi import APIRouter

from app.services.travel_service import (
    TravelPlannerService
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

    result = service.run_trip_planner(

        request.dict()
    )

    return {

        "chat_summary":
        result.get(
            "final_response"
        ),

        "itinerary":
        result.get(
            "optimized_itinerary"
        ),

        "flights":
        result.get(
            "flight_options",
            []
        ),

        "hotels":
        result.get(
            "hotel_options",
            []
        ),

        "transports":
        result.get(
            "transport_options",
            []
        ),

        "policy":
        result.get(
            "policy_results",
            {}
        ),

        "approval":
        result.get(
            "approval_workflow",
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