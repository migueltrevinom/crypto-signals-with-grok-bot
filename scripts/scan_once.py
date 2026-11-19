"""One scan of the monitored pairs. Prints new entry signals as JSON lines.

The Grok Bot box runs this. It does not place orders and does not read
exchange API keys. Without Mongo it scans BTC, ETH, SOL, and ARB on
Binance and KuCoin and still prints JSON.
"""

import asyncio
import json
from datetime import UTC, datetime, timedelta

from Repositories.MarketData.modules.market_module import load_candles
from Repositories.Signals.modules.engine_module import LADDER, build_entries

DEFAULTS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "ARBUSDT")
EXCHANGES = ("binance", "kucoin")


async def scan(echo: bool = True) -> list[dict]:
    found: list[dict] = []
    start = datetime.now(UTC) - timedelta(days=800)
    window = datetime.now(UTC) - timedelta(days=14)
    for exchange in EXCHANGES:
        for symbol in DEFAULTS:
            series = {}
            for timeframe in LADDER:
                series[timeframe] = await load_candles(exchange, symbol, timeframe, start)
            entries = build_entries(exchange, symbol, series, window_start=window)
            for entry in entries:
                payload = {
                    "signal_id": entry.signal_id,
                    "type": "entry_plan",
                    "exchange": entry.exchange,
                    "symbol": entry.symbol,
                    "timeframe": entry.timeframe,
                    "direction": entry.direction,
                    "close_time": entry.close_time.isoformat(),
                    "price": entry.price,
                    "stop": entry.stop,
                    "level": entry.level,
                    "atr": entry.atr,
                    "score": entry.score,
                    "strategy_version": entry.strategy_version,
                }
                found.append(payload)
                if echo:
                    print(json.dumps(payload))
    return found


def main() -> None:
    asyncio.run(scan(echo=True))


if __name__ == "__main__":
    main()
