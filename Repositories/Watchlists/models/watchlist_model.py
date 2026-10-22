"""Symbols and timeframes to scan. Collection `watchlists`."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel

Market = Literal["spot", "futures"]


def _utcnow() -> datetime:
    return datetime.now(UTC)


class WatchlistSymbol(BaseModel):
    symbol: str
    exchange: str = "binance"
    market: Market = "spot"


class Watchlist(Document):
    name: str
    symbols: list[WatchlistSymbol] = Field(default_factory=list)
    timeframes: list[str] = Field(default_factory=list)
    ltf_map: dict[str, str] = Field(default_factory=dict)
    strategy_key: str = "time_mode"
    strategy_config_id: PydanticObjectId | None = None
    alert_channel_ids: list[PydanticObjectId] = Field(default_factory=list)
    enabled: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "watchlists"
        indexes = [
            IndexModel([("enabled", ASCENDING)], name="enabled"),
        ]
