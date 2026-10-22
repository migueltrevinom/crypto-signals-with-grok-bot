"""A cross-venue spread net of costs. This is not an order."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ArbitrageOpportunity(Document):
    status: Literal["new", "stale", "dismissed"] = "new"
    detected_at: datetime = Field(default_factory=_utcnow)
    expires_at: datetime | None = None
    base_asset: str
    quote_asset: str
    path_kind: Literal["cross_exchange_spot", "cex_dex"]
    legs: list[dict[str, Any]] = Field(default_factory=list)
    gross_spread_bps: float
    net_spread_bps: float
    costs: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "arbitrage_opportunities"
        indexes = [
            IndexModel(
                [("status", ASCENDING), ("detected_at", ASCENDING)],
                name="status_detected",
            ),
            IndexModel(
                [
                    ("base_asset", ASCENDING),
                    ("quote_asset", ASCENDING),
                    ("detected_at", ASCENDING),
                ],
                name="pair_detected",
            ),
        ]
