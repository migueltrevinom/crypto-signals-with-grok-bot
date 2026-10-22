"""Show the planning seeds. Phase 2 reads app_settings through build_query."""

from typing import Any

from Core.planning_seeds import (
    ARBITRAGE_SETTINGS,
    LADDER_TIMEFRAMES,
    PREFERRED_QUOTE_ASSETS,
    SMA_FILTER_TIMEFRAME,
    SMA_LENGTH,
)
from Core.prototype_config import load_prototype_config


def _wrap(key: str, value: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": None,
        "key": key,
        "version": 0,
        "active": True,
        "persisted": False,
        "value": value,
    }


async def show_ladder(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    return _wrap(
        "ladder",
        {
            "timeframes": LADDER_TIMEFRAMES,
            "sma_filter_timeframe": SMA_FILTER_TIMEFRAME,
            "sma_length": SMA_LENGTH,
            "decision_timeframes": ["1w", "3d", "1d"],
            "entry_timeframes": ["4h", "6h", "8h"],
            "context_timeframe": "1M",
            "alignment": "binance",
        },
    )


async def show_scanner(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    config = load_prototype_config()
    return _wrap(
        "scanner",
        {
            "history_bars": config["history_bars"],
            "report_window_bars": config["report_window_bars"],
            "state_retention_days": config["state_retention_days"],
            "data_sources": config["data_sources"],
            "preferred_quote_assets": PREFERRED_QUOTE_ASSETS,
        },
    )


async def show_arbitrage(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    return _wrap("arbitrage", dict(ARBITRAGE_SETTINGS))
