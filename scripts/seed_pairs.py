"""Load USDT spot pairs from Binance and KuCoin into Mongo.

Default monitored bases are BTC, ETH, SOL, and ARB on both exchanges.
Requires Mongo. Does not use API keys.
"""

import asyncio

from app.documents import DOCUMENT_MODELS
from Core.database import connect, disconnect
from Repositories.Pairs.modules.pair_module import seed_pairs


async def _run() -> None:
    await connect(DOCUMENT_MODELS)
    try:
        counts = await seed_pairs()
        print(counts)
    finally:
        await disconnect()


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
