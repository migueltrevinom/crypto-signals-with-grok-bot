"""Reserved. No arbitrage rules exist yet. Do not register this model."""

from datetime import datetime
from typing import Any, Literal

from beanie import Document
from pydantic import Field


class ArbitrageOpportunity(Document):
    status: Literal["new", "dismissed"] = "new"
    detected_at: datetime | None = None
    legs: list[dict[str, Any]] = Field(default_factory=list)
    notes: str = ""

    class Settings:
        name = "arbitrage_opportunities"
