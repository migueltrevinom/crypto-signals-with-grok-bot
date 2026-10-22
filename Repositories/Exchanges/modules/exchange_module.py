"""Kline source list.

Planning skeleton: reads prototype/config.json. It does not call build_query.
Phase 2 reads `exchange_sources` through Core.mongo_orm.build_query.
"""

from typing import Any

from Core.prototype_config import load_prototype_config

# Base URLs match prototype/data.py. An unknown name stays in the order with a null URL.
BASE_URLS = {
    "binance": "https://api.binance.com",
    "binance_vision": "https://data-api.binance.vision",
    "bybit": "https://api.bybit.com",
    "okx": "https://www.okx.com",
}


async def list_sources(auth_user: dict | None = None) -> list[dict[str, Any]]:
    del auth_user
    config = load_prototype_config()
    sources: list[dict[str, Any]] = []
    for index, name in enumerate(config["data_sources"], start=1):
        sources.append(
            {
                "name": name,
                "priority": index,
                "kind": "spot_klines",
                "base_url": BASE_URLS.get(name),
                "market": "spot",
                "enabled": True,
                "auth": "none",
            }
        )
    return sources
