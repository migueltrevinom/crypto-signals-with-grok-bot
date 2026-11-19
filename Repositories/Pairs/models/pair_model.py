"""One exchange listing. Public market data only."""

from datetime import UTC, datetime

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Pair(Document):
    exchange: str
    symbol: str
    base_asset: str
    quote_asset: str
    venue_symbol: str
    market: str = "spot"
    monitored: bool = False
    status: str = "trading"
    taker_fee: float = 0.001
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "pairs"
        indexes = [
            IndexModel(
                [("exchange", ASCENDING), ("symbol", ASCENDING)],
                unique=True,
                name="exchange_symbol",
            ),
            IndexModel([("monitored", ASCENDING)], name="monitored"),
        ]
