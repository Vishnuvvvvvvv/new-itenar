from app.graph.state import (
    TravelState
)
from app.graph.agent_runtime import (
    run_agent_step
)

from app.agents.transport_agent import (
    transport_agent
)


def transport_node(
    state: TravelState
):
    run_agent_step(
        state,
        "Transport Agent",
        "Selecting local transport by coverage area, comfort, efficiency, and cost."
    )

    hotels = state.get(
        "hotel_options",
        []
    )

    cities = list(

        set(

            hotel.get("city")

            for hotel in hotels
        )
    )

    transports = transport_agent(
        cities
    )

    state[
        "transport_options"
    ] = transports

    run_agent_step(
        state,
        "Transport Agent",
        f"Selected {len(transports)} local transport recommendation(s)."
    )

    return state
