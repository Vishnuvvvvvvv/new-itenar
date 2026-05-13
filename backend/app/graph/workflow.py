from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.state import (
    TravelState
)

# =========================
# NODES
# =========================

from app.graph.nodes.parser_node import (
    parser_node
)

from app.graph.nodes.context_node import (
    context_node
)

from app.graph.nodes.supervisor_node import (
    supervisor_node
)

from app.graph.nodes.flight_node import (
    flight_node
)

from app.graph.nodes.calendar_node import (
    calendar_node
)

from app.graph.nodes.hotel_node import (
    hotel_node
)

from app.graph.nodes.optimizer_node import (
    optimizer_node
)

from app.graph.nodes.transport_node import (
    transport_node
)

from app.graph.nodes.policy_node import (
    policy_node
)

from app.graph.nodes.approval_node import (
    approval_node
)

from app.graph.nodes.explanation_node import (
    explanation_node
)

# =========================
# GRAPH
# =========================

workflow = StateGraph(
    TravelState
)

# =========================
# ADD NODES
# =========================

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
    "flight",
    flight_node
)

workflow.add_node(
    "calendar",
    calendar_node
)

workflow.add_node(
    "hotel",
    hotel_node
)

workflow.add_node(
    "optimizer",
    optimizer_node
)

workflow.add_node(
    "transport",
    transport_node
)

workflow.add_node(
    "policy",
    policy_node
)

workflow.add_node(
    "approval",
    approval_node
)

workflow.add_node(
    "explanation",
    explanation_node
)

# =========================
# ENTRY
# =========================

workflow.set_entry_point(
    "parser"
)

# =========================
# FLOW
# =========================

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
    "flight"
)

workflow.add_edge(
    "flight",
    "calendar"
)

workflow.add_edge(
    "calendar",
    "hotel"
)

workflow.add_edge(
    "hotel",
    "optimizer"
)

workflow.add_edge(
    "optimizer",
    "transport"
)

workflow.add_edge(
    "transport",
    "policy"
)

workflow.add_edge(
    "policy",
    "approval"
)

workflow.add_edge(
    "approval",
    "explanation"
)

workflow.add_edge(
    "explanation",
    END
)

# =========================
# COMPILE
# =========================

graph = workflow.compile()