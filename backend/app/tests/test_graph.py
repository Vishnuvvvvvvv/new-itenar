from app.graph.workflow import graph
initial_state = {

    "user_input": """
    I need to travel from Chennai to Bangalore,
    then Hyderabad,
    then Mumbai for client meetings next week.

    Avoid morning flights and prefer business hotels.
    """,

    "employee_id": "EMP001",

    "parsed_request": {},

    "request_type": "",

    "next_steps": [],

    "employee_context": {},

    "calendar_events": [],

    "calendar_conflicts": [],

    "flight_options": [],

    "hotel_options": [],

    "transport_options": [],

    "optimized_itinerary": {},

    "policy_results": {},

    "approval_workflow": {},

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