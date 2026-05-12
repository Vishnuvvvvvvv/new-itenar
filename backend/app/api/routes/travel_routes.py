from fastapi import APIRouter

from app.schemas.travel_schema import (
    TravelRequest,
    TravelResponse
)

from app.services.travel_service import (
    TravelPlannerService
)


router = APIRouter()


@router.post(
    "/plan-trip",
    response_model=TravelResponse
)
def plan_trip(

    request: TravelRequest
):

    result = (
        TravelPlannerService
        .generate_itinerary(
            request.user_input,
            request.employee_id
        )
    )

    return {

        "final_response": result[
            "final_response"
        ],

        "request_type": result[
            "request_type"
        ],

        "employee_context": result[
            "employee_context"
        ],

        "flight_options": result[
            "flight_options"
        ],

        "hotel_options": result[
            "hotel_options"
        ],

        "policy_results": result[
            "policy_results"
        ],

        "optimized_itinerary": result[
            "optimized_itinerary"
        ],

        "execution_logs": result[
            "execution_logs"
        ]
    }