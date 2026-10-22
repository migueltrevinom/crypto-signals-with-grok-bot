"""Reserved futures position. Not registered with Beanie until that phase.

Stop and size stay nullable on purpose. The charts do not show them.
"""

from datetime import datetime
from typing import Literal

from beanie import Document


class Position(Document):
    symbol: str
    market: Literal["futures"] = "futures"
    side: Literal["long", "short"]
    status: Literal["open", "closed"] = "open"
    entry_price: float | None = None
    size: float | None = None
    stop: float | None = None
    opened_at: datetime | None = None
    closed_at: datetime | None = None

    class Settings:
        name = "positions"
