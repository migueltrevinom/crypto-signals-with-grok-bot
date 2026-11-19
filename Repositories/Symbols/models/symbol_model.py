"""One pair to monitor, with a listing per venue. Any quote asset is allowed."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Listing(BaseModel):
    venue_kind: Literal["cex", "dex"]
    venue: str
    venue_symbol: str
    status: Literal["trading", "halted"] = "trading"


class Symbol(Document):
    base_asset: str
    quote_asset: str
    market: Literal["spot", "futures"] = "spot"
    enabled: bool = True
    tags: list[str] = Field(default_factory=list)
    priority: int = 100
    listings: list[Listing] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "symbols"
        indexes = [
            IndexModel(
                [
                    ("base_asset", ASCENDING),
                    ("quote_asset", ASCENDING),
                    ("market", ASCENDING),
                ],
                unique=True,
                name="pair",
            ),
            IndexModel([("enabled", ASCENDING), ("priority", ASCENDING)], name="scan_order"),
            IndexModel(
                [("listings.venue", ASCENDING), ("listings.venue_symbol", ASCENDING)],
                name="listing",
            ),
        ]
