from app.graph.state import TravelState


def export_node(state: TravelState):

    state["final_response"] = (
        "Itinerary exported successfully."
    )

    state["execution_logs"].append(
        "Export node executed."
    )

    return state