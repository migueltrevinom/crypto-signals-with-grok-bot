"""Short-lived quote used to explain an opportunity. TTL is one day."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class VenueQuote(Document):
    venue_kind: Literal["cex", "dex"]
    venue: str
    venue_symbol: str
    bid: float | None = None
    ask: float | None = None
    fee_bps: float | None = None
    gas_quote: float | None = None
    quoted_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "venue_quotes"
        indexes = [
            IndexModel(
                [
                    ("venue", ASCENDING),
                    ("venue_symbol", ASCENDING),
                    ("quoted_at", ASCENDING),
                ],
                name="venue_symbol_time",
            ),
            IndexModel(
                [("quoted_at", ASCENDING)],
                name="quoted_at_ttl",
                expireAfterSeconds=86400,
            ),
        ]
