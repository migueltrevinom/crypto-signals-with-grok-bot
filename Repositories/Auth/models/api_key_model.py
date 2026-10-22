"""User API key. Only the hash is stored."""

from datetime import UTC, datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ApiKey(Document):
    user_id: PydanticObjectId
    prefix: str = "cs_live"
    last4: str
    key_hash: Indexed(str, unique=True)
    scopes: list[str] = Field(default_factory=list)
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "api_keys"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("revoked_at", ASCENDING)],
                name="user_revoked",
            ),
        ]
