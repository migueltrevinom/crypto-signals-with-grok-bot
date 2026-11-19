"""Binance public spot klines. Falls back to data-api.binance.vision."""

from datetime import UTC, datetime

from Core.http_client import get_json
from Repositories.MarketData.modules.candles import CandleBar, ms, utc_from_ms

BINANCE_URLS = (
    "https://api.binance.com",
    "https://data-api.binance.vision",
)
INTERVALS = {
    "1h": "1h",
    "4h": "4h",
    "6h": "6h",
    "8h": "8h",
    "1d": "1d",
    "3d": "3d",
    "1w": "1w",
    "1M": "1M",
}


def parse_klines(symbol: str, timeframe: str, rows: list) -> list[CandleBar]:
    now = datetime.now(UTC)
    bars: list[CandleBar] = []
    for row in rows:
        bar = CandleBar(
            exchange="binance",
            symbol=symbol,
            timeframe=timeframe,
            open_time=utc_from_ms(int(row[0])),
            open=float(row[1]),
            high=float(row[2]),
            low=float(row[3]),
            close=float(row[4]),
            volume=float(row[5]),
        )
        if bar.close_time > now:
            continue
        bars.append(bar)
    bars.sort(key=lambda bar: bar.open_time)
    return bars


async def fetch_klines(
    symbol: str,
    timeframe: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[CandleBar]:
    interval = INTERVALS[timeframe]
    start_ms = ms(start) if start else None
    end_ms = ms(end) if end else None
    collected: list[CandleBar] = []
    cursor = start_ms
    last_error: Exception | None = None
    for base in BINANCE_URLS:
        collected = []
        cursor = start_ms
        try:
            while True:
                params: dict[str, object] = {
                    "symbol": symbol,
                    "interval": interval,
                    "limit": 1000,
                }
                if cursor is not None:
                    params["startTime"] = cursor
                if end_ms is not None:
                    params["endTime"] = end_ms
                payload = await get_json(f"{base}/api/v3/klines", params=params)
                if isinstance(payload, dict):
                    raise RuntimeError(str(payload))
                batch = parse_klines(symbol, timeframe, payload)
                if not batch:
                    break
                collected.extend(batch)
                if len(payload) < 1000:
                    break
                cursor = int(batch[-1].close_time.timestamp() * 1000)
                if end_ms is not None and cursor > end_ms:
                    break
            if collected:
                return _dedupe(collected)
        except Exception as exc:
            last_error = exc
            continue
    raise RuntimeError(f"binance klines failed for {symbol} {timeframe}: {last_error}")


async def list_usdt_spot_symbols() -> list[str]:
    payload = await get_json("https://api.binance.com/api/v3/exchangeInfo")
    names: list[str] = []
    for row in payload.get("symbols", []):
        if row.get("quoteAsset") != "USDT" or row.get("status") != "TRADING":
            continue
        if row.get("isSpotTradingAllowed") is False:
            continue
        names.append(row["symbol"])
    return sorted(names)


def _dedupe(bars: list[CandleBar]) -> list[CandleBar]:
    seen: dict[datetime, CandleBar] = {}
    for bar in bars:
        seen[bar.open_time] = bar
    return [seen[key] for key in sorted(seen)]
