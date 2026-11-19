"""Measured result for one log row. Does not rewrite the log."""

from datetime import datetime
from typing import Literal

from beanie import Document, Indexed, PydanticObjectId
from pymongo import ASCENDING, IndexModel


class Outcome(Document):
    signal_log_id: Indexed(PydanticObjectId, unique=True)
    status: Literal["open", "stopped", "target_hit", "exited", "expired"]
    r_multiple: float | None = None
    closed_at: datetime | None = None
    source: Literal["forward", "backtest"]

    class Settings:
        name = "outcomes"
        indexes = [
            IndexModel(
                [("source", ASCENDING), ("closed_at", ASCENDING)],
                name="source_closed",
            ),
        ]
