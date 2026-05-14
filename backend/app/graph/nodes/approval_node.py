from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.approval_agent import (
    approval_agent
)


def approval_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Approval Agent",
        "Applying deterministic approval rules for policy, budget, class, and hotel category."
    )

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

    state["approval_prompt_pending"] = (
        approval_result.get("approval_required", False)
        and approval_result.get("status") == "pending"
    )

    run_agent_step(
        state,
        "Approval Agent",
        f"Approval status: {approval_result.get('status')}."
    )

    return state
