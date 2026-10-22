"""Process-local cache placeholder.

Phase 1 can keep a short-lived candle cache here or in the `candles`
collection. The collection is the one that survives a restart. This module
is the in-process helper if a hot path needs it. Not used by the skeleton.
"""

from typing import Any

_store: dict[str, Any] = {}


def get(key: str) -> Any | None:
    return _store.get(key)


def set(key: str, value: Any) -> None:
    _store[key] = value


def clear() -> None:
    _store.clear()
