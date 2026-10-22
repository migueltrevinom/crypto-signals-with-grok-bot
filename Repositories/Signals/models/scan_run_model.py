"""One scanner pass. Collection `scan_runs`."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document
from pydantic import Field
from pymongo import DESCENDING, IndexModel

ScanStatus = Literal["running", "completed", "failed"]


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ScanRun(Document):
    started_at: datetime
    finished_at: datetime | None = None
    status: ScanStatus = "running"
    sources: dict[str, int] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    symbols: list[str] = Field(default_factory=list)
    timeframes: list[str] = Field(default_factory=list)
    signals_found: int = 0
    signals_new: int = 0
    strategy_key: str = "time_mode"
    strategy_version: int | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "scan_runs"
        indexes = [
            IndexModel([("started_at", DESCENDING)], name="started_at_desc"),
        ]
