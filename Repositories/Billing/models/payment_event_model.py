"""Provider webhook, stored once. No card numbers."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class PaymentEvent(Document):
    provider: str
    provider_event_id: Indexed(str, unique=True)
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    processed_at: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "payment_events"
