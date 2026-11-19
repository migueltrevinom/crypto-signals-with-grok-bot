"""KuCoin public spot klines. No API key.

KuCoin's type enum has 4hour, 6hour, 8hour, 1day, 1week, and 1month.
It has no 3day. Monthly candles are not used: 1M is resampled from 1day
so the bucket matches Binance's calendar month. 3d is resampled from 1day
on Binance's 3-day epoch grid.
"""

from datetime import UTC, datetime

from Core.http_client import get_json
from Repositories.MarketData.modules.candles import CandleBar, ms, utc_from_ms

TYPES = {
    "1h": "1hour",
    "4h": "4hour",
    "6h": "6hour",
    "8h": "8hour",
    "1d": "1day",
    "1w": "1week",
    "1M": "1month",
}


def to_venue_symbol(symbol: str) -> str:
    if "-" in symbol:
        return symbol
    if not symbol.endswith("USDT"):
        raise ValueError(f"KuCoin mapping needs an explicit venue symbol for {symbol}")
    return f"{symbol[:-4]}-USDT"


def from_venue_symbol(venue_symbol: str) -> str:
    base, quote = venue_symbol.split("-")
    return f"{base}{quote}"


def parse_klines(symbol: str, timeframe: str, rows: list) -> list[CandleBar]:
    """KuCoin rows are [start_sec, open, close, high, low, amount, volume], newest first."""
    now = datetime.now(UTC)
    bars: list[CandleBar] = []
    for row in rows:
        bar = CandleBar(
            exchange="kucoin",
            symbol=symbol,
            timeframe=timeframe,
            open_time=utc_from_ms(int(row[0]) * 1000),
            open=float(row[1]),
            high=float(row[3]),
            low=float(row[4]),
            close=float(row[2]),
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
    if timeframe not in TYPES:
        raise ValueError(f"KuCoin has no native {timeframe}; resample it")
    venue = to_venue_symbol(symbol)
    end_sec = int(ms(end) / 1000) if end else None
    start_sec = int(ms(start) / 1000) if start else None
    collected: list[CandleBar] = []
    guard = 0
    while guard < 40:
        guard += 1
        params: dict[str, object] = {"symbol": venue, "type": TYPES[timeframe]}
        if start_sec is not None:
            params["startAt"] = start_sec
        if end_sec is not None:
            params["endAt"] = end_sec
        payload = await get_json("https://api.kucoin.com/api/v1/market/candles", params=params)
        if payload.get("code") != "200000":
            raise RuntimeError(f"kucoin error: {payload.get('msg')}")
        rows = payload.get("data") or []
        batch = parse_klines(symbol, timeframe, rows)
        if not batch:
            break
        collected.extend(batch)
        if len(rows) < 1500:
            break
        oldest = ms(batch[0].open_time) // 1000
        if start_sec is not None and oldest <= start_sec:
            break
        end_sec = oldest - 1
    return _dedupe(collected)


async def list_usdt_spot_symbols() -> list[str]:
    payload = await get_json("https://api.kucoin.com/api/v2/symbols")
    if payload.get("code") != "200000":
        raise RuntimeError(f"kucoin symbols: {payload.get('msg')}")
    names: list[str] = []
    for row in payload.get("data") or []:
        if row.get("quoteCurrency") != "USDT":
            continue
        if row.get("enableTrading") is False:
            continue
        names.append(from_venue_symbol(row["symbol"]))
    return sorted(set(names))


def _dedupe(bars: list[CandleBar]) -> list[CandleBar]:
    seen: dict[datetime, CandleBar] = {}
    for bar in bars:
        seen[bar.open_time] = bar
    return [seen[key] for key in sorted(seen)]
