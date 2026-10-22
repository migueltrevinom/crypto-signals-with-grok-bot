"""Ordered public kline source. Collection `exchange_sources`."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, Indexed
from pydantic import Field

Market = Literal["spot", "futures"]
AuthKind = Literal["none", "api_key"]


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ExchangeSource(Document):
    name: Indexed(str, unique=True)
    priority: int
    kind: str = "spot_klines"
    base_url: str
    market: Market = "spot"
    enabled: bool = True
    auth: AuthKind = "none"
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "exchange_sources"
