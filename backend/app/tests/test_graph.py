from app.graph.workflow import graph

initial_state = {


    "user_input": """
  Plan a Bangalore business trip next week.

Avoid morning flights.

Prefer business hotels near office.
    """,

    "employee_id": "EMP001",

    "employee_context": {},

    "parsed_request": {},

    "next_steps": [],

    "current_step": "",

    "request_type": "",

    "calendar_events": [],

    "calendar_conflicts": [],

    "flight_options": [],

    "hotel_options": [],

    "policy_results": {},

    "optimized_itinerary": {},

    "final_response": "",

    "execution_logs": []

}


result = graph.invoke(initial_state)

print("\nFINAL RESPONSE:\n")

print(result["final_response"])

print("\nEXECUTION LOGS:\n")

for log in result["execution_logs"]:

    print(log)


print("\nREQUEST TYPE:\n")

print(result["request_type"])

print("\nNEXT STEPS:\n")

print(result["next_steps"])


print("\nEMPLOYEE CONTEXT:\n")

print(result["employee_context"])


print("\nFLIGHT OPTIONS:\n")

for flight in result["flight_options"]:

    print(flight)

print("\nHOTEL OPTIONS:\n")

for hotel in result["hotel_options"]:

    print(hotel)

print("\nPOLICY RESULTS:\n")

print(result["policy_results"])


print("\nOPTIMIZED ITINERARY:\n")

print(result["optimized_itinerary"])