"""Build higher timeframes on Binance's grid. Closed buckets only."""

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from Repositories.MarketData.modules.candles import INTERVAL_MS, CandleBar, ms, utc_from_ms


def _bucket_open_ms(open_ms: int, target: str) -> int:
    if target == "1M":
        dt = utc_from_ms(open_ms)
        month_open = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return ms(month_open)
    if target == "1w":
        dt = utc_from_ms(open_ms)
        monday = (dt - timedelta(days=dt.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return ms(monday)
    step = INTERVAL_MS[target]
    return (open_ms // step) * step


def resample(
    candles: list[CandleBar],
    source_timeframe: str,
    target_timeframe: str,
    *,
    now: datetime | None = None,
) -> list[CandleBar]:
    """Aggregate `source_timeframe` bars into `target_timeframe`.

    The last bucket is dropped when it has not closed yet, and when it does
    not contain a full set of source bars (a short 3d bucket is not emitted).
    """
    if not candles:
        return []
    now = now or datetime.now(UTC)
    grouped: dict[int, list[CandleBar]] = defaultdict(list)
    for bar in candles:
        grouped[_bucket_open_ms(ms(bar.open_time), target_timeframe)].append(bar)
    expected = 1
    if target_timeframe != "1M":
        expected = INTERVAL_MS[target_timeframe] // INTERVAL_MS[source_timeframe]
    out: list[CandleBar] = []
    for open_ms in sorted(grouped):
        group = sorted(grouped[open_ms], key=lambda bar: bar.open_time)
        sample = group[0]
        built = CandleBar(
            exchange=sample.exchange,
            symbol=sample.symbol,
            timeframe=target_timeframe,
            open_time=utc_from_ms(open_ms),
            open=group[0].open,
            high=max(bar.high for bar in group),
            low=min(bar.low for bar in group),
            close=group[-1].close,
            volume=sum(bar.volume for bar in group),
            origin="resampled",
            source_timeframe=source_timeframe,
        )
        complete = len(group) >= expected
        if target_timeframe == "1M":
            complete = group[-1].close_time >= built.close_time
        if complete and built.close_time <= now:
            out.append(built)
    return out
