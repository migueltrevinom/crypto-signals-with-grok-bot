"""Load a closed candle series, resampling when the venue has no native bar."""

from datetime import UTC, datetime

from Repositories.MarketData.modules import binance, kucoin
from Repositories.MarketData.modules.candles import RESAMPLE_FROM, CandleBar
from Repositories.MarketData.modules.resample_module import resample

ADAPTERS = {"binance": binance, "kucoin": kucoin}


async def load_candles(
    exchange: str,
    symbol: str,
    timeframe: str,
    start: datetime | None = None,
    end: datetime | None = None,
    *,
    now: datetime | None = None,
) -> list[CandleBar]:
    adapter = ADAPTERS[exchange]
    source = RESAMPLE_FROM.get(exchange, {}).get(timeframe)
    if source:
        native = await load_candles(exchange, symbol, source, start, end, now=now)
        return resample(native, source, timeframe, now=now or datetime.now(UTC))
    bars = await adapter.fetch_klines(symbol, timeframe, start, end)
    moment = now or datetime.now(UTC)
    return [bar for bar in bars if bar.close_time <= moment]
