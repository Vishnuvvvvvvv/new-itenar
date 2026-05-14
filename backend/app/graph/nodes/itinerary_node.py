from app.graph.state import (
    TravelState,
)
from app.graph.agent_runtime import (
    run_agent_step,
)
from app.services.itinerary_engine import (
    build_day_wise_itinerary,
)


def itinerary_node(state: TravelState):
    run_agent_step(
        state,
        "Itinerary Engine",
        "Building day-wise timeline with flights, hotels, transport, meetings, policy, and approval status."
    )
    state["itinerary_days"] = build_day_wise_itinerary(
        state.get("parsed_request", {}),
        state.get("optimized_itinerary", {}),
        state.get("transport_options", []),
        state.get("calendar_analysis", {}),
        state.get("policy_results", {}),
        state.get("approval_workflow", {}),
    )
    run_agent_step(
        state,
        "Itinerary Engine",
        f"Generated {len(state['itinerary_days'])} itinerary day(s)."
    )
    return state
