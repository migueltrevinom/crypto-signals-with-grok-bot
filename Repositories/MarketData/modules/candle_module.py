"""Candle reads and the closed-candle cache.

The list route is still a placeholder. `cache_bars` upserts into `candles`
when Mongo is reachable. A missing database does not fail a backtest.
"""

from pymongo import UpdateOne

from Core.config import get_settings
from Core.http import empty_page, page_args
from Repositories.MarketData.modules.candles import CandleBar


async def get(params: dict, auth_user: dict | None = None) -> dict:
    del auth_user
    page, limit = page_args(params)
    return empty_page(page, limit)


async def cache_bars(bars: list[CandleBar]) -> int:
    if not bars:
        return 0
    from motor.motor_asyncio import AsyncIOMotorClient

    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=400)
    try:
        await client.admin.command("ping")
        collection = client[settings.mongodb_db]["candles"]
        await collection.create_index(
            [("exchange", 1), ("symbol", 1), ("timeframe", 1), ("open_time", 1)],
            unique=True,
            name="candle_identity",
        )
        ops = [
            UpdateOne(
                {
                    "exchange": bar.exchange,
                    "symbol": bar.symbol,
                    "timeframe": bar.timeframe,
                    "open_time": bar.open_time,
                },
                {
                    "$set": {
                        "close_time": bar.close_time,
                        "open": bar.open,
                        "high": bar.high,
                        "low": bar.low,
                        "close": bar.close,
                        "volume": bar.volume,
                        "origin": bar.origin,
                        "source_timeframe": bar.source_timeframe,
                    }
                },
                upsert=True,
            )
            for bar in bars
        ]
        result = await collection.bulk_write(ops, ordered=False)
        return result.upserted_count + result.modified_count
    except Exception:
        return 0
    finally:
        client.close()
