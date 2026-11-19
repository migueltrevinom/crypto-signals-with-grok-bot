"""One proposed entry. Not an order."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class EntryPlan(Document):
    symbol_id: PydanticObjectId | None = None
    direction: Literal["long", "short"]
    score: float
    components: dict[str, Any] = Field(default_factory=dict)
    timeframe_in_control: str
    entry_timeframe: str
    decision_hits: list[str] = Field(default_factory=list)
    sma_6h_side: Literal["above", "below"]
    signal_ids: list[str] = Field(default_factory=list)
    status: Literal["proposed", "accepted", "rejected", "expired"] = "proposed"
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "entry_plans"
        indexes = [
            IndexModel(
                [
                    ("symbol_id", ASCENDING),
                    ("status", ASCENDING),
                    ("created_at", ASCENDING),
                ],
                name="symbol_status",
            ),
        ]
