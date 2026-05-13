from app.graph.state import (
    TravelState
)

from app.agents.approval_agent import (
    approval_agent
)


def approval_node(
    state: TravelState
):

    optimized_itinerary = state.get(
        "optimized_itinerary",
        {}
    )

    policy_results = state.get(
        "policy_results",
        {}
    )

    approval_result = approval_agent(

        optimized_itinerary,

        policy_results
    )

    state["approval_workflow"] = (
        approval_result
    )

    state["execution_logs"].append(
        "Approval agent executed successfully."
    )

    return state