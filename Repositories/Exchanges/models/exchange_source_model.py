"""Ordered public kline source. Collection `exchange_sources`."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, Indexed
from pydantic import Field

Market = Literal["spot", "futures"]
AuthKind = Literal["none", "api_key"]
SymbolStyle = Literal["concat", "dash", "alias"]


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
    symbol_style: SymbolStyle = "concat"
    native_timeframes: list[str] = Field(default_factory=list)
    resample_from: dict[str, str] = Field(default_factory=dict)
    maker_fee_bps: float | None = None
    taker_fee_bps: float | None = None
    withdrawal_fees: dict[str, float] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "exchange_sources"
