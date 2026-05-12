from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.state import TravelState

from app.graph.router import (
    dynamic_router
)

from app.graph.nodes.parser_node import (
    parser_node
)

from app.graph.nodes.context_node import (
    context_node
)

from app.graph.nodes.supervisor_node import (
    supervisor_node
)

from app.graph.nodes.router_node import (
    router_node
)

from app.graph.nodes.calendar_node import (
    calendar_node
)

from app.graph.nodes.flight_node import (
    flight_node
)

from app.graph.nodes.hotel_node import (
    hotel_node
)

from app.graph.nodes.policy_node import (
    policy_node
)

from app.graph.nodes.optimizer_node import (
    optimizer_node
)

from app.graph.nodes.explanation_node import (
    explanation_node
)

from app.graph.nodes.export_node import (
    export_node
)

from app.graph.nodes.booking_node import (
    booking_node
)


workflow = StateGraph(TravelState)


# ====================================
# ADD NODES
# ====================================

workflow.add_node(
    "parser",
    parser_node
)

workflow.add_node(
    "context",
    context_node
)

workflow.add_node(
    "supervisor",
    supervisor_node
)

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "calendar",
    calendar_node
)

workflow.add_node(
    "flight",
    flight_node
)

workflow.add_node(
    "hotel",
    hotel_node
)

workflow.add_node(
    "policy",
    policy_node
)

workflow.add_node(
    "optimizer",
    optimizer_node
)

workflow.add_node(
    "explanation",
    explanation_node
)

workflow.add_node(
    "export",
    export_node
)

workflow.add_node(
    "booking",
    booking_node
)


# ====================================
# ENTRY POINT
# ====================================

workflow.set_entry_point(
    "parser"
)


# ====================================
# INITIAL FLOW
# ====================================

workflow.add_edge(
    "parser",
    "context"
)

workflow.add_edge(
    "context",
    "supervisor"
)

workflow.add_edge(
    "supervisor",
    "router"
)


# ====================================
# DYNAMIC ROUTING
# ====================================

workflow.add_conditional_edges(

    "router",

    dynamic_router,

    {
        "calendar": "calendar",

        "flight": "flight",

        "hotel": "hotel",

        "policy": "policy",

        "optimizer": "optimizer",

        "explanation": "explanation",

        "export": "export",

        "booking": "booking",

        "end": END
    }
)


# ====================================
# RETURN TO ROUTER
# ====================================

workflow.add_edge(
    "calendar",
    "router"
)

workflow.add_edge(
    "flight",
    "router"
)

workflow.add_edge(
    "hotel",
    "router"
)

workflow.add_edge(
    "policy",
    "router"
)

workflow.add_edge(
    "optimizer",
    "router"
)

workflow.add_edge(
    "explanation",
    END
)

workflow.add_edge(
    "export",
    END
)

workflow.add_edge(
    "booking",
    END
)


# ====================================
# COMPILE GRAPH
# ====================================

graph = workflow.compile()