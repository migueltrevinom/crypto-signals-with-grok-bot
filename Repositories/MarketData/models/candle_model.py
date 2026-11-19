"""Optional closed-candle cache. Exchanges remain the source of truth."""

from datetime import datetime
from typing import Literal

from beanie import Document
from pymongo import ASCENDING, IndexModel


class Candle(Document):
    exchange: str
    symbol: str
    timeframe: str
    open_time: datetime
    close_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    origin: Literal["native", "resampled"] = "native"
    source_timeframe: str | None = None

    class Settings:
        name = "candles"
        indexes = [
            IndexModel(
                [
                    ("exchange", ASCENDING),
                    ("symbol", ASCENDING),
                    ("timeframe", ASCENDING),
                    ("open_time", ASCENDING),
                ],
                unique=True,
                name="candle_identity",
            ),
        ]
