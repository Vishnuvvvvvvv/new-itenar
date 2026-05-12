from app.graph.state import TravelState


def booking_node(state: TravelState):

    state["final_response"] = (
        "Booking completed successfully."
    )

    state["execution_logs"].append(
        "Booking node executed."
    )

    return state