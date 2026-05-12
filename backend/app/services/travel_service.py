from app.graph.workflow import graph


class TravelPlannerService:

    @staticmethod
    def generate_itinerary(

        user_input,

        employee_id
    ):

        initial_state = {

            "user_input": user_input,

            "employee_id": employee_id,

            "parsed_request": {},

            "calendar_events": [],

            "calendar_conflicts": [],

            "flight_options": [],

            "hotel_options": [],

            "policy_results": {},

            "optimized_itinerary": {},

            "final_response": "",

            "execution_logs": [],

            "next_steps": [],

            "request_type": "",

            "employee_context": {}
        }

        result = graph.invoke(
            initial_state
        )

        return result