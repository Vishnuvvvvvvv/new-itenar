from app.db.mock_transport_db import (
    get_transport_options
)


def transport_agent(
    cities
):
    selected_transports = []

    for city in cities:
        transport_options = get_transport_options(
            city
        )

        if not transport_options:
            continue

        selected_transports.append(
            _select_best_transport(
                transport_options
            )
        )

    return selected_transports


def _select_best_transport(
    transport_options
):
    ranked = sorted(
        transport_options,
        key=lambda transport: (
            transport.get("comfort_level", "") != "high",
            transport.get("estimated_cost", 999999),
        )
    )

    selected = dict(ranked[0])
    selected["reason"] = (
        "Deterministic selection based on comfort, coverage area, and cost."
    )
    return selected
