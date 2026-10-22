"""Active time@mode configuration.

Planning skeleton. Detection stays in prototype/timemode.py.
`sma_filter_timeframe` is forced to 6h. The ladder is the resolved one,
not prototype/config.json `ltf_map`. The prototype file is not modified.
"""

from typing import Any

from Core.planning_seeds import LADDER_TIMEFRAMES, SMA_FILTER_TIMEFRAME
from Core.prototype_config import load_prototype_config


async def show_active(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    config = load_prototype_config()
    params = dict(config["params"])
    params["sma_filter_timeframe"] = SMA_FILTER_TIMEFRAME
    return {
        "id": None,
        "key": "time_mode",
        "version": 0,
        "active": True,
        "persisted": False,
        "source": "prototype/config.json overlaid with resolved decisions",
        "params": params,
        "scanner": {
            "history_bars": config["history_bars"],
            "report_window_bars": config["report_window_bars"],
            "data_sources": config["data_sources"],
            "state_retention_days": config["state_retention_days"],
        },
        "ladder": {
            "timeframes": LADDER_TIMEFRAMES,
            "sma_filter_timeframe": SMA_FILTER_TIMEFRAME,
        },
    }
