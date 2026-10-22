"""Where a signal is delivered. `config` is secret and must not be logged."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AlertChannel(Document):
    name: str
    kind: Literal["grok_chat", "webhook", "email"] = "grok_chat"
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "alert_channels"
