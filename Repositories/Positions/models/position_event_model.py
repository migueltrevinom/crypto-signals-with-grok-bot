"""Lifecycle log for a planned position."""

from datetime import UTC, datetime
from typing import Any, Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class PositionEvent(Document):
    position_id: PydanticObjectId
    type: Literal[
        "planned",
        "stop_moved",
        "target_hit",
        "exit_signal",
        "stopped",
        "cancelled",
        "note",
    ]
    price: float | None = None
    size: float | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "position_events"
        indexes = [
            IndexModel(
                [("position_id", ASCENDING), ("created_at", ASCENDING)],
                name="position_created",
            ),
        ]
