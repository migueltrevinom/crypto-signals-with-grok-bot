"""One simulated fill. Fees and slippage are stored on the row."""

from datetime import datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pymongo import ASCENDING, IndexModel


class PaperFill(Document):
    account_id: PydanticObjectId
    signal_log_id: PydanticObjectId
    side: Literal["long", "short"]
    fill_price: float
    fee_quote: float
    slippage_bps: float
    opened_at: datetime
    closed_at: datetime | None = None
    r_multiple: float | None = None

    class Settings:
        name = "paper_fills"
        indexes = [
            IndexModel(
                [("account_id", ASCENDING), ("signal_log_id", ASCENDING)],
                unique=True,
                name="account_log",
            ),
        ]
