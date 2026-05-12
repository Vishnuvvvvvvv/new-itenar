from app.graph.state import TravelState


def calendar_node(state: TravelState):

    state["execution_logs"].append(
        "Calendar node executed."
    )

    return state