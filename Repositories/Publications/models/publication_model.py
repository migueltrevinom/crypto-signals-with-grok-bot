"""When a user is allowed to see one logged signal."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Publication(Document):
    signal_log_id: PydanticObjectId
    user_id: PydanticObjectId
    plan_code: str
    release_at: datetime
    status: Literal["scheduled", "released", "suppressed"] = "scheduled"
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "publications"
        indexes = [
            IndexModel(
                [("signal_log_id", ASCENDING), ("user_id", ASCENDING)],
                unique=True,
                name="log_user",
            ),
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("release_at", ASCENDING),
                    ("status", ASCENDING),
                ],
                name="user_release",
            ),
        ]
