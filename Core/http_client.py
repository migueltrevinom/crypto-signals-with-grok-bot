"""Outbound HTTP. Exchange klines move here in the scanner port.

The behavior to port is prototype/data.py: try each source, keep closed
candles only, retry, then fall through. This function is the single client
those fetchers should use.
"""

from typing import Any


async def get_json(url: str, timeout: float = 15.0) -> Any:
    del url, timeout
    raise NotImplementedError(
        "HTTP fetch is ported with MarketData. See prototype/data.py and docs/roadmap.md."
    )
