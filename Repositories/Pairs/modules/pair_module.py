"""Seed and list monitored USDT spot pairs. No credentials."""

from datetime import UTC, datetime

from Repositories.MarketData.modules.kucoin import to_venue_symbol
from Repositories.MarketData.modules.market_module import ADAPTERS
from Repositories.Pairs.models.pair_model import Pair

DEFAULT_BASES = ("BTC", "ETH", "SOL", "ARB")


def _split(symbol: str) -> tuple[str, str]:
    if not symbol.endswith("USDT"):
        raise ValueError(symbol)
    return symbol[:-4], "USDT"


async def seed_pairs() -> dict[str, int]:
    """Load every USDT spot pair. Monitor BTC, ETH, SOL, and ARB on both venues."""
    counts = {"inserted": 0, "updated": 0}
    for exchange, adapter in ADAPTERS.items():
        symbols = await adapter.list_usdt_spot_symbols()
        for symbol in symbols:
            base, quote = _split(symbol)
            venue = to_venue_symbol(symbol) if exchange == "kucoin" else symbol
            monitored = base in DEFAULT_BASES
            existing = await Pair.find_one(Pair.exchange == exchange, Pair.symbol == symbol)
            now = datetime.now(UTC)
            if existing is None:
                await Pair(
                    exchange=exchange,
                    symbol=symbol,
                    base_asset=base,
                    quote_asset=quote,
                    venue_symbol=venue,
                    monitored=monitored,
                    updated_at=now,
                ).insert()
                counts["inserted"] += 1
            else:
                existing.monitored = monitored
                existing.venue_symbol = venue
                existing.updated_at = now
                await existing.save()
                counts["updated"] += 1
    return counts


async def monitored_pairs(exchange: str | None = None) -> list[Pair]:
    query = Pair.find(Pair.monitored == True)  # noqa: E712
    if exchange:
        query = query.find(Pair.exchange == exchange)
    return await query.to_list()
