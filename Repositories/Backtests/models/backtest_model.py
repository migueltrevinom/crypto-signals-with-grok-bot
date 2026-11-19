"""A historical run of the same detector. Collection `backtests`."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Backtest(Document):
    name: str
    strategy_key: str = "time_mode"
    strategy_version: int | None = None
    params_snapshot: dict[str, Any] = Field(default_factory=dict)
    symbols: list[str] = Field(default_factory=list)
    timeframes: list[str] = Field(default_factory=list)
    start: datetime
    end: datetime
    status: Literal["queued", "running", "completed", "failed"] = "queued"
    summary: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    finished_at: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "backtests"
        indexes = [
            IndexModel([("status", ASCENDING), ("created_at", ASCENDING)], name="status_created"),
        ]
