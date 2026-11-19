"""Versioned Mongo settings. Ladder, scanner, symbols, arbitrage, auth."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AppSetting(Document):
    key: Indexed(str)
    version: int
    active: bool = False
    value: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "app_settings"
        indexes = [
            IndexModel(
                [("key", ASCENDING), ("version", ASCENDING)],
                unique=True,
                name="key_version",
            ),
        ]
