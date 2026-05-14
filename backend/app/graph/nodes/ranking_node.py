from app.agents.ranking_agent import (
    rank_recommendations,
)
from app.graph.state import (
    TravelState,
)
from app.graph.agent_runtime import (
    run_agent_step,
)


def ranking_node(state: TravelState):
    run_agent_step(
        state,
        "Ranking Agent",
        "Scoring flights, hotels, and transport from 0-100 for business suitability."
    )
    parsed = state.get(
        "parsed_request",
        {}
    )

    ranking_results = rank_recommendations(
        state.get("flight_options", []),
        state.get("hotel_options", []),
        state.get("transport_options", []),
        parsed.get("preferences", []),
        state.get("policy_results", {}),
    )

    state["ranking_results"] = ranking_results
    state["flight_options"] = ranking_results.get("flights", [])
    state["hotel_options"] = ranking_results.get("hotels", [])
    state["transport_options"] = ranking_results.get("transports", [])
    run_agent_step(
        state,
        "Ranking Agent",
        "Ranking scores and explanations generated."
    )
    return state
