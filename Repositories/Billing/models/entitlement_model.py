"""Effective features for one user, synced from Stripe. Reads use this row."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Entitlement(Document):
    user_id: Indexed(PydanticObjectId, unique=True)
    features: dict[str, Any] = Field(default_factory=dict)
    source: Literal["stripe", "seed"] = "seed"
    synced_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "entitlements"
