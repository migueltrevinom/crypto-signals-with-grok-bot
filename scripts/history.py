"""Candle history with a local cache so the matrix can be rerun."""

import json
from datetime import UTC, datetime
from pathlib import Path

from Core.config import REPO_ROOT
from Repositories.MarketData.modules.candles import CandleBar, utc_from_ms
from Repositories.MarketData.modules.market_module import load_candles

CACHE = REPO_ROOT / "reports" / ".cache"
TIMEFRAMES = ("4h", "6h", "8h", "1d", "3d", "1w", "1M")


def _path(exchange: str, symbol: str, timeframe: str) -> Path:
    return CACHE / exchange / symbol / f"{timeframe}.json"


def _dump(bars: list[CandleBar], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "exchange": bar.exchange,
            "symbol": bar.symbol,
            "timeframe": bar.timeframe,
            "open_ms": int(bar.open_time.timestamp() * 1000),
            "o": bar.open,
            "h": bar.high,
            "l": bar.low,
            "c": bar.close,
            "v": bar.volume,
            "origin": bar.origin,
            "source_timeframe": bar.source_timeframe,
        }
        for bar in bars
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")


def _load(path: Path) -> list[CandleBar]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [
        CandleBar(
            exchange=row["exchange"],
            symbol=row["symbol"],
            timeframe=row["timeframe"],
            open_time=utc_from_ms(row["open_ms"]),
            open=row["o"],
            high=row["h"],
            low=row["l"],
            close=row["c"],
            volume=row["v"],
            origin=row.get("origin", "native"),
            source_timeframe=row.get("source_timeframe"),
        )
        for row in rows
    ]


async def get_series(
    exchange: str,
    symbol: str,
    start: datetime,
    *,
    refresh: bool = False,
) -> dict[str, list[CandleBar]]:
    series: dict[str, list[CandleBar]] = {}
    for timeframe in TIMEFRAMES:
        path = _path(exchange, symbol, timeframe)
        if path.exists() and not refresh:
            series[timeframe] = _load(path)
            continue
        bars = await load_candles(exchange, symbol, timeframe, start, datetime.now(UTC))
        _dump(bars, path)
        from Repositories.MarketData.modules.candle_module import cache_bars

        await cache_bars(bars)
        series[timeframe] = bars
    return series
