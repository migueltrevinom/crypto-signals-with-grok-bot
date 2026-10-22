"""Append-only signal record. Rows are not updated."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class SignalLog(Document):
    seq: Indexed(int, unique=True)
    signal_id: str
    candle_close_time: datetime
    strategy_version: str
    payload: dict[str, Any]
    prev_hash: str
    chain_hash: str
    corrects_seq: int | None = None
    logged_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "signal_logs"
        indexes = [
            IndexModel([("logged_at", ASCENDING)], name="logged_at"),
            IndexModel([("candle_close_time", ASCENDING)], name="candle_close"),
        ]
