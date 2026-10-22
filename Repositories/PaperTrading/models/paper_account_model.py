"""House track record or a personal simulation. They are not mixed."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class PaperAccount(Document):
    kind: Literal["house", "personal"]
    owner_user_id: PydanticObjectId | None = None
    forward_started_at: datetime | None = None
    fee_bps: float = 10
    slippage_bps: float = 5
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "paper_accounts"
        indexes = [
            IndexModel(
                [("kind", ASCENDING), ("owner_user_id", ASCENDING)],
                name="kind_owner",
            ),
        ]
