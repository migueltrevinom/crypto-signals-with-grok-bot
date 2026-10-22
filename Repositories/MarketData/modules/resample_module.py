"""Build a higher timeframe from lower closed candles.

Planning placeholder. The rules (Binance grid, drop the forming bar, OHLC
aggregation) are in docs/repositories.md. No resampling runs in this pass.
"""

from typing import Any


def resample(
    candles: list[dict[str, Any]],
    source_timeframe: str,
    target_timeframe: str,
) -> list[dict]:
    del candles, source_timeframe, target_timeframe
    raise NotImplementedError(
        "Resampling is specified in docs/repositories.md and is not implemented yet."
    )
