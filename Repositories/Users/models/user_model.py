"""Account. Roles and password hashes are stored here. Tokens are not."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class User(Document):
    name: str
    email: str | None = None
    password_hash: str | None = None
    role: Literal["owner", "admin", "subscriber", "free"] = "free"
    status: Literal["active", "disabled"] = "active"
    email_verified: bool = False
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True, sparse=True, name="email"),
            IndexModel([("role", ASCENDING), ("status", ASCENDING)], name="role_status"),
        ]
