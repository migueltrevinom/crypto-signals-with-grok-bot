"""Normalized closed candle. Exchange adapters all return this shape."""

from datetime import UTC, datetime
from typing import Any

LADDER = ("4h", "6h", "8h", "1d", "3d", "1w", "1M")

INTERVAL_MS = {
    "1h": 3_600_000,
    "4h": 14_400_000,
    "6h": 21_600_000,
    "8h": 28_800_000,
    "1d": 86_400_000,
    "3d": 259_200_000,
    "1w": 604_800_000,
}

# KuCoin has no 3d. Its 1month type exists, but monthly opens are not the
# Binance calendar grid, so 1M is built from 1d. See docs in the module.
RESAMPLE_FROM = {
    "binance": {},
    "kucoin": {"3d": "1d", "1M": "1d"},
}


def utc_from_ms(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=UTC)


def ms(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return int(dt.timestamp() * 1000)


class CandleBar:
    def __init__(
        self,
        *,
        exchange: str,
        symbol: str,
        timeframe: str,
        open_time: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: float,
        origin: str = "native",
        source_timeframe: str | None = None,
    ) -> None:
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.open_time = open_time.astimezone(UTC)
        step = INTERVAL_MS.get(timeframe)
        if timeframe == "1M":
            year = self.open_time.year + (1 if self.open_time.month == 12 else 0)
            month = 1 if self.open_time.month == 12 else self.open_time.month + 1
            close_at = self.open_time.replace(year=year, month=month, day=1)
            self.close_time = close_at
        elif step is None:
            raise ValueError(f"unknown timeframe {timeframe}")
        else:
            self.close_time = utc_from_ms(ms(self.open_time) + step)
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.origin = origin
        self.source_timeframe = source_timeframe

    def as_dict(self) -> dict[str, Any]:
        return {
            "t": ms(self.open_time),
            "ct": ms(self.close_time),
            "o": self.open,
            "h": self.high,
            "l": self.low,
            "c": self.close,
            "v": self.volume,
        }
