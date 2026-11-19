"""One signal from a backtest. Split out so a long run stays under 16 MB."""

from datetime import datetime
from typing import Any

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


class BacktestEvent(Document):
    backtest_id: PydanticObjectId
    signal_id: str
    type: str
    symbol: str
    timeframe: str
    direction: str
    close_time: datetime
    payload: dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "backtest_events"
        indexes = [
            IndexModel(
                [("backtest_id", ASCENDING), ("close_time", ASCENDING)],
                name="backtest_close",
            ),
        ]
