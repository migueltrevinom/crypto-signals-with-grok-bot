"""A DEX quote source. Swaps are not sent from this domain."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, Indexed
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class DexVenue(Document):
    name: Indexed(str, unique=True)
    kind: Literal["dex_pool", "dex_aggregator"]
    chain: str
    protocol: str = ""
    quote_method: Literal["pool_mid", "aggregator_quote"]
    enabled: bool = False
    gas_units: int | None = None
    taker_fee_bps: float | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "dex_venues"
