"""Weights and thresholds for the entry score."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ConfluenceConfig(Document):
    key: Indexed(str)
    version: int
    active: bool = False
    decision_timeframes: list[str] = Field(default_factory=list)
    entry_timeframes: list[str] = Field(default_factory=list)
    require_sma_6h: bool = True
    weights: dict[str, Any] = Field(default_factory=dict)
    thresholds: dict[str, float] = Field(default_factory=dict)
    entry_timeframe_priority: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "confluence_configs"
        indexes = [
            IndexModel(
                [("key", ASCENDING), ("version", ASCENDING)],
                unique=True,
                name="key_version",
            ),
        ]
