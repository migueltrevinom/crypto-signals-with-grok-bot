"""A subscriber's bot URL. The signing secret is stored as a hash."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class WebhookEndpoint(Document):
    user_id: PydanticObjectId
    url: str
    secret_hash: str
    format: Literal["generic", "3commas", "wundertrading", "cornix", "altrady"] = "generic"
    enabled: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "webhook_endpoints"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("enabled", ASCENDING)],
                name="user_enabled",
            ),
        ]
