"""One feed row per subject per channel kind. The Grok Bot polls these."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Alert(Document):
    channel_id: PydanticObjectId | None = None
    channel_kind: Literal["grok_chat", "webhook", "email"] = "grok_chat"
    subject_type: Literal["signal", "entry_plan", "position", "arbitrage_opportunity"]
    subject_id: str
    status: Literal["pending", "delivered", "acked", "failed"] = "pending"
    attempts: int = 0
    last_error: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    delivered_at: datetime | None = None
    acked_at: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "alerts"
        indexes = [
            IndexModel(
                [
                    ("subject_type", ASCENDING),
                    ("subject_id", ASCENDING),
                    ("channel_kind", ASCENDING),
                ],
                unique=True,
                name="subject_channel",
            ),
            IndexModel(
                [
                    ("channel_kind", ASCENDING),
                    ("status", ASCENDING),
                    ("created_at", ASCENDING),
                ],
                name="feed",
            ),
        ]
