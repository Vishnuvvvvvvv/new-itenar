from app.graph.workflow import (
    graph
)


class TravelPlannerService:

    def run_trip_planner(

        self,
        request_data
    ):

        initial_state = {

            "user_input":
            request_data.get(
                "user_input"
            ),

            "employee_id":
            request_data.get(
                "employee_id"
            ),

            "parsed_input": {},

            "employee_context": {},

            "request_type": "",

            "flight_options": [],

            "hotel_options": [],

            "transport_options": [],

            "policy_results": {},

            "approval_workflow": {},

            "optimized_itinerary": {},

            "calendar_analysis": {},

            "final_response": "",

            "execution_logs": []
        }

        result = graph.invoke(
            initial_state
        )

        return result