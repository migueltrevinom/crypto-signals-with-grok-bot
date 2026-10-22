"""Optional subset of symbol ids. The ladder is not stored here."""

from datetime import UTC, datetime

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Watchlist(Document):
    name: str
    symbol_ids: list[PydanticObjectId] = Field(default_factory=list)
    strategy_key: str = "time_mode"
    enabled: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "watchlists"
        indexes = [
            IndexModel([("enabled", ASCENDING)], name="enabled"),
        ]
