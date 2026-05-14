import os
import time


def run_agent_step(
    state,
    agent_name,
    detail
):
    delay = float(
        os.getenv(
            "AGENT_STEP_DELAY_SECONDS",
            "0.45"
        )
    )

    state.setdefault(
        "execution_logs",
        []
    ).append(
        f"{agent_name}: {detail}"
    )

    if delay > 0:
        time.sleep(
            delay
        )
