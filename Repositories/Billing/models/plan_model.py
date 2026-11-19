"""Sellable tier. price_cents stays null until pricing is chosen."""

from datetime import UTC, datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Plan(Document):
    code: Indexed(str, unique=True)
    name: str
    public: bool = True
    currency: str = "cad"
    interval: str = "month"
    price_cents: int | None = None
    trial_days: int = 0
    grace_days: int = 0
    entitlements: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "plans"
