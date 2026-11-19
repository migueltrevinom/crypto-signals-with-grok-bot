"""Refresh token hash. The raw token is returned once and not stored."""

from datetime import UTC, datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class RefreshToken(Document):
    user_id: PydanticObjectId
    token_hash: Indexed(str, unique=True)
    expires_at: datetime
    revoked_at: datetime | None = None
    replaced_by: PydanticObjectId | None = None
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "refresh_tokens"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("expires_at", ASCENDING)],
                name="user_expires",
            ),
        ]
