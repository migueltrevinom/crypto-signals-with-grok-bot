"""Append-only audit row. Not updated."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AuditLog(Document):
    actor_id: PydanticObjectId | None = None
    action: str
    target_type: str
    target_id: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)
    ip: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "audit_logs"
        indexes = [
            IndexModel([("created_at", ASCENDING)], name="created_at"),
            IndexModel(
                [("actor_id", ASCENDING), ("created_at", ASCENDING)],
                name="actor_created",
            ),
            IndexModel(
                [("action", ASCENDING), ("created_at", ASCENDING)],
                name="action_created",
            ),
        ]
