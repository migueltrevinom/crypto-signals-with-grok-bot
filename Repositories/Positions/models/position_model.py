"""A planned trade. No order is submitted from this document."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class PositionTarget(BaseModel):
    price: float
    r_multiple: float
    size_fraction: float = 0.5
    status: Literal["open", "hit", "cancelled"] = "open"


class Position(Document):
    user_id: PydanticObjectId | None = None
    symbol_id: PydanticObjectId | None = None
    venue: str | None = None
    market: Literal["spot", "futures"] = "spot"
    strategy_key: str = "time_mode"
    entry_plan_id: PydanticObjectId | None = None
    signal_ids: list[str] = Field(default_factory=list)
    risk_profile_id: PydanticObjectId | None = None
    side: Literal["long", "short"]
    status: Literal[
        "planned",
        "active",
        "stopped",
        "target_hit",
        "exited",
        "cancelled",
    ] = "planned"
    entry_price: float | None = None
    entry_timeframe: str | None = None
    timeframe_in_control: str | None = None
    stop_price: float | None = None
    stop_method: str | None = None
    size_base: float | None = None
    notional_quote: float | None = None
    risk_amount: float | None = None
    leverage: float = 1
    targets: list[PositionTarget] = Field(default_factory=list)
    opened_at: datetime | None = None
    closed_at: datetime | None = None
    close_reason: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "positions"
        indexes = [
            IndexModel([("status", ASCENDING), ("created_at", ASCENDING)], name="status_created"),
            IndexModel([("symbol_id", ASCENDING), ("status", ASCENDING)], name="symbol_status"),
            IndexModel([("user_id", ASCENDING), ("status", ASCENDING)], name="user_status"),
        ]
