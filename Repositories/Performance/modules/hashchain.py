"""Append-only hash chain for signal logs.

chain_hash = sha256(prev_hash + canonical_json(payload))
The first prev_hash is 64 zero hex digits. Rows are insert-only.
"""

import hashlib
import json
from typing import Any

GENESIS = "0" * 64


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def chain_hash(prev_hash: str, payload: dict[str, Any]) -> str:
    raw = (prev_hash + canonical_json(payload)).encode()
    return hashlib.sha256(raw).hexdigest()


def signal_key(
    *,
    exchange: str,
    symbol: str,
    timeframe: str,
    direction: str,
    close_ms: int,
    level: float,
) -> str:
    text = f"entry_plan|{exchange}|{symbol}|{timeframe}|{direction}|{close_ms}|{level:.10g}"
    return hashlib.sha1(text.encode()).hexdigest()[:16]
