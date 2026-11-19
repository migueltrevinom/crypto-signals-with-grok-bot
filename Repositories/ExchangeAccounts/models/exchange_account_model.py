"""Encrypted trade-only venue key. Unused until that phase. No withdrawals."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ExchangeAccount(Document):
    user_id: PydanticObjectId
    venue: str
    ciphertext: str
    nonce: str
    key_id: str
    withdrawal_enabled: bool | None = None
    status: Literal["disabled", "active"] = "disabled"
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "exchange_accounts"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("venue", ASCENDING)],
                name="user_venue",
            ),
        ]
