from app.graph.workflow import (
    graph
)


class TravelPlannerService:

    def run_trip_planner(

        self,
        request_data
    ):

        initial_state = {

            "session_id":
            request_data.get(
                "session_id",
                ""
            ),

            "user_input":
            request_data.get(
                "user_input"
            ),

            "employee_id":
            request_data.get(
                "employee_id"
            ),

            "conversation_history":
            request_data.get(
                "conversation_history",
                []
            ),

            "previous_request":
            request_data.get(
                "previous_request",
                {}
            ),

            "parsed_request": {},

            "employee_context": {},

            "request_type": "",

            "flight_options": [],

            "hotel_options": [],

            "transport_options": [],

            "ranking_results": {},

            "policy_results": {},

            "approval_workflow": {},

            "optimized_itinerary": {},

            "itinerary_days": [],

            "calendar_analysis": {},

            "booking_state":
            request_data.get(
                "booking_state",
                {}
            ),

            "approval_prompt_pending": False,

            "recommendation_warnings": [],

            "final_response": "",

            "execution_logs": []
        }

        result = graph.invoke(
            initial_state
        )

        return result
