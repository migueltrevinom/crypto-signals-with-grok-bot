"""Paper trades for entry signals. No live orders.

One open trade per exchange and symbol. A later signal while that trade is
open is logged and not entered. Exit is the stop, or two closes back inside
the level with the prototype's lower-low (higher-high) sequence.
"""

from dataclasses import dataclass
from datetime import datetime

from Repositories.MarketData.modules.candles import CandleBar

TAKER_FEE = {"binance": 0.001, "kucoin": 0.001}
DEFAULT_SLIPPAGE_BPS = 5.0
DEFAULT_EQUITY = 10_000.0
RISK_FRACTION = 0.01
STOP_BUFFER_ATR = 0.25


@dataclass
class EntrySignal:
    exchange: str
    symbol: str
    timeframe: str
    direction: str
    close_time: datetime
    price: float
    level: float
    atr: float
    stop: float
    score: float
    signal_id: str
    candle_low: float
    candle_high: float
    strategy_version: str
    inputs: dict


@dataclass
class PaperTrade:
    signal_id: str
    exchange: str
    symbol: str
    timeframe: str
    direction: str
    opened_at: datetime
    closed_at: datetime
    entry: float
    stop: float
    exit: float
    exit_reason: str
    size: float
    pnl: float
    r_multiple: float
    fee: float
    regime: str = ""


def protective_stop(
    direction: str, price: float, level: float, extreme: float, atr: float
) -> float:
    buffer = STOP_BUFFER_ATR * atr
    if direction == "long":
        anchor = min(level, extreme)
        stop = anchor - buffer
        if stop >= price:
            stop = price - buffer
        return stop
    anchor = max(level, extreme)
    stop = anchor + buffer
    if stop <= price:
        stop = price + buffer
    return stop


def _fill(price: float, direction: str, slippage_bps: float, *, entering: bool) -> float:
    slip = slippage_bps / 10_000
    worse = slip if (direction == "long") == entering else -slip
    return price * (1 + worse)


def simulate(
    entries: list[EntrySignal],
    bars_by_tf: dict[str, list[CandleBar]],
    *,
    equity: float = DEFAULT_EQUITY,
    slippage_bps: float = DEFAULT_SLIPPAGE_BPS,
) -> tuple[list[PaperTrade], float]:
    entries = sorted(entries, key=lambda item: item.close_time)
    open_until: datetime | None = None
    trades: list[PaperTrade] = []
    for entry in entries:
        if open_until is not None and entry.close_time < open_until:
            continue
        series = bars_by_tf.get(entry.timeframe, [])
        if not any(bar.close_time > entry.close_time for bar in series):
            continue
        risk = equity * RISK_FRACTION
        stop_distance = abs(entry.price - entry.stop)
        if stop_distance <= 0 or risk <= 0:
            continue
        size = risk / stop_distance
        entry_fill = _fill(entry.price, entry.direction, slippage_bps, entering=True)
        exit_price, exit_time, reason = _walk_exit(entry, series)
        exit_fill = _fill(exit_price, entry.direction, slippage_bps, entering=False)
        fee_rate = TAKER_FEE.get(entry.exchange, 0.001)
        fee = (entry_fill + exit_fill) * size * fee_rate
        sign = 1 if entry.direction == "long" else -1
        pnl = size * (exit_fill - entry_fill) * sign - fee
        gross = (exit_price - entry.price) * sign
        r_multiple = (pnl / risk) if risk else 0.0
        if gross == 0 and pnl == 0:
            r_multiple = 0.0
        equity += pnl
        open_until = exit_time
        trades.append(
            PaperTrade(
                signal_id=entry.signal_id,
                exchange=entry.exchange,
                symbol=entry.symbol,
                timeframe=entry.timeframe,
                direction=entry.direction,
                opened_at=entry.close_time,
                closed_at=exit_time,
                entry=entry_fill,
                stop=entry.stop,
                exit=exit_fill,
                exit_reason=reason,
                size=size,
                pnl=pnl,
                r_multiple=r_multiple,
                fee=fee,
            )
        )
        if equity <= 0:
            break
    return trades, equity


def _walk_exit(entry: EntrySignal, bars: list[CandleBar]) -> tuple[float, datetime, str]:
    level = entry.level
    long = entry.direction == "long"
    start = 0
    for index, bar in enumerate(bars):
        if bar.close_time > entry.close_time:
            start = index
            break
    else:
        last = bars[-1]
        return last.close, last.close_time, "open_at_end"
    for index in range(start, len(bars)):
        bar = bars[index]
        if long and bar.low <= entry.stop:
            return entry.stop, bar.close_time, "stop"
        if not long and bar.high >= entry.stop:
            return entry.stop, bar.close_time, "stop"
        if index < 2:
            continue
        prev, before = bars[index - 1], bars[index - 2]
        if prev.close_time <= entry.close_time:
            continue
        if long:
            inside = bar.close < level and prev.close < level
            sequence = bar.low < prev.low and prev.low < before.low
        else:
            inside = bar.close > level and prev.close > level
            sequence = bar.high > prev.high and prev.high > before.high
        if inside and sequence:
            return bar.close, bar.close_time, "two_lower_closes"
    last = bars[-1]
    return last.close, last.close_time, "open_at_end"
