"""Track-record placeholder. The log writer is not implemented."""

from typing import Any

from Core.planning_seeds import DISCLAIMER


async def track_record(sample: str = "forward") -> dict[str, Any]:
    return {
        "disclaimer": DISCLAIMER,
        "sample": sample,
        "forward_started_at": None,
        "trades": 0,
        "win_rate": None,
        "average_r": None,
        "max_drawdown_r": None,
    }
