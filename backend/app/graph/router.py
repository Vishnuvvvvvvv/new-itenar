from app.graph.state import TravelState


def dynamic_router(
    state: TravelState
):

    next_steps = state["next_steps"]

    if not next_steps:

        return "end"

    next_node = next_steps.pop(0)

    state["current_step"] = next_node

    return next_node