"""One signed POST. Not created before the publication's release_at."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class WebhookDelivery(Document):
    endpoint_id: PydanticObjectId
    publication_id: PydanticObjectId
    idempotency_key: Indexed(str, unique=True)
    status: Literal["pending", "delivered", "failed"] = "pending"
    attempts: int = 0
    next_attempt_at: datetime | None = None
    last_error: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "webhook_deliveries"
