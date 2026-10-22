"""Stop, size, leverage, and targets. Most specific enabled row wins."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class RiskProfile(Document):
    name: str
    user_id: PydanticObjectId | None = None
    strategy_key: str | None = "time_mode"
    symbol_id: PydanticObjectId | None = None
    market: Literal["spot", "futures", "any"] = "any"
    enabled: bool = True
    risk_per_trade: dict[str, Any] = Field(default_factory=dict)
    account: dict[str, Any] = Field(default_factory=dict)
    max_leverage: float = 1
    max_notional_quote: float | None = None
    stop: dict[str, Any] = Field(default_factory=dict)
    trailing: dict[str, Any] = Field(default_factory=dict)
    take_profit: dict[str, Any] = Field(default_factory=dict)
    exit: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "risk_profiles"
        indexes = [
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("strategy_key", ASCENDING),
                    ("symbol_id", ASCENDING),
                    ("market", ASCENDING),
                    ("enabled", ASCENDING),
                ],
                name="resolution",
            ),
        ]
