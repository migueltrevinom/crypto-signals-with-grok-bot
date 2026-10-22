"""Stored time@mode signal. Collection `signals`. See docs/data-model.md."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel

SignalType = Literal[
    "mode_confirmed",
    "bias_flip",
    "mode_expiry",
    "block_breakout_entry",
    "exit",
]
Direction = Literal["bullish", "bearish", "long", "short"]
LevelKind = Literal["mode", "block"]
SignalStatus = Literal["new", "acknowledged", "dismissed"]
Market = Literal["spot", "futures"]


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Signal(Document):
    signal_id: Indexed(str, unique=True)
    type: SignalType
    symbol: str
    timeframe: str
    direction: Direction
    close_time: datetime
    close_time_edmonton: str
    price: float
    level: float
    level_kind: LevelKind
    atr: float
    atr_distance: float
    tradingview_url: str
    details: dict[str, Any] = Field(default_factory=dict)
    strategy_key: str = "time_mode"
    market: Market = "spot"
    status: SignalStatus = "new"
    scan_run_id: PydanticObjectId | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "signals"
        indexes = [
            IndexModel(
                [("symbol", ASCENDING), ("timeframe", ASCENDING), ("close_time", ASCENDING)],
                name="symbol_tf_close",
            ),
            IndexModel(
                [("type", ASCENDING), ("close_time", ASCENDING)],
                name="type_close",
            ),
            IndexModel(
                [("status", ASCENDING), ("close_time", ASCENDING)],
                name="status_close",
            ),
        ]
