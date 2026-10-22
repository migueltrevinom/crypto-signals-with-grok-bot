"""Active time@mode configuration.

Planning skeleton: reads prototype/config.json and does not persist it.
Detection functions are not ported yet. They stay in prototype/timemode.py
until roadmap phase 1. This module must stay a pure reader of parameters;
fetching and saving belong to other domains, called from the worker.
"""

from typing import Any

from Core.prototype_config import load_prototype_config


async def show_active(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    config = load_prototype_config()
    return {
        "id": None,
        "key": "time_mode",
        "version": 0,
        "active": True,
        "persisted": False,
        "source": "prototype/config.json",
        "params": config["params"],
        "scanner": {
            "history_bars": config["history_bars"],
            "report_window_bars": config["report_window_bars"],
            "data_sources": config["data_sources"],
            "ltf_map": config["ltf_map"],
            "state_retention_days": config["state_retention_days"],
        },
        "symbols": config["symbols"],
        "timeframes": config["timeframes"],
    }
