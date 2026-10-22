"""Versioned time@mode parameters. Collection `strategy_configs`."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ScannerSettings(BaseModel):
    history_bars: int = 1000
    report_window_bars: int = 3
    data_sources: list[str] = Field(
        default_factory=lambda: ["binance", "binance_vision", "bybit", "okx"]
    )
    state_retention_days: int = 120


class StrategyConfig(Document):
    key: Indexed(str)
    version: int
    active: bool = False
    params: dict[str, Any] = Field(default_factory=dict)
    scanner: ScannerSettings = Field(default_factory=ScannerSettings)
    notes: str = ""
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "strategy_configs"
        indexes = [
            IndexModel(
                [("key", ASCENDING), ("version", ASCENDING)],
                unique=True,
                name="key_version",
            ),
        ]
