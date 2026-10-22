"""One delivery per signal per channel. Collection `alerts`."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Alert(Document):
    signal_id: str
    channel_id: PydanticObjectId
    status: Literal["pending", "sent", "failed"] = "pending"
    attempts: int = 0
    last_error: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    sent_at: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "alerts"
        indexes = [
            IndexModel(
                [("signal_id", ASCENDING), ("channel_id", ASCENDING)],
                unique=True,
                name="signal_channel",
            ),
        ]
