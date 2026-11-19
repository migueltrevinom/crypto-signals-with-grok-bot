"""Paper trades. No live orders.

One open trade per pair. A second signal while that trade is open is blocked,
unless the exit setting closes on an opposite signal and then reverses.
Exit rules are a setting: baseline (fixed stop or two closes), trail,
opposite signal, or two closes only.
"""

from dataclasses import dataclass, field
from datetime import datetime

from Repositories.MarketData.modules.candles import CandleBar

TAKER_FEE = {"binance": 0.001, "kucoin": 0.001}
DEFAULT_SLIPPAGE_BPS = 5.0
DEFAULT_EQUITY = 10_000.0
RISK_FRACTION = 0.01
STOP_BUFFER_ATR = 0.25

EXIT_MODES = {
    "baseline": {"stop": True, "trail": False, "opposite": False, "two_close": True},
    "trail": {"stop": True, "trail": True, "opposite": False, "two_close": False},
    "opposite": {"stop": True, "trail": False, "opposite": True, "two_close": False},
    "two_close": {"stop": False, "trail": False, "opposite": False, "two_close": True},
    "all": {"stop": True, "trail": True, "opposite": True, "two_close": True},
}


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
class TrailLevel:
    time: datetime
    price: float
    direction: str
    kind: str


@dataclass
class PaperTrade:
    signal_id: str
    exchange: str
    symbol: str
    timeframe: str
    direction: str
    opened_at: datetime
    closed_at: datetime | None
    entry: float
    stop: float
    exit: float | None
    exit_reason: str
    size: float
    pnl: float
    r_multiple: float
    fee: float
    realized: bool
    entry_fee: float = 0.0
    regime: str = ""
    variant: str = ""


@dataclass
class SimResult:
    trades: list[PaperTrade] = field(default_factory=list)
    blocked: int = 0
    equity: float = DEFAULT_EQUITY


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


def stop_beyond(
    direction: str, price: float, anchor: float, atr: float, buffer_atr: float
) -> float | None:
    """Stop beyond a structure price by a whole number of ATRs.

    Returns None when the anchor is already on the wrong side of price, so a
    variant does not invent a stop that the structure did not give it.
    """
    if atr <= 0 or buffer_atr <= 0:
        return None
    buffer = buffer_atr * atr
    if direction == "long":
        stop = anchor - buffer
        return stop if stop < price else None
    stop = anchor + buffer
    return stop if stop > price else None


def _fill(price: float, direction: str, slippage_bps: float, *, entering: bool) -> float:
    slip = slippage_bps / 10_000
    worse = slip if (direction == "long") == entering else -slip
    return price * (1 + worse)


class _Open:
    def __init__(
        self, entry: EntrySignal, fill: float, size: float, risk: float, fee: float
    ) -> None:
        self.entry = entry
        self.fill = fill
        self.size = size
        self.risk = risk
        self.entry_fee = fee
        self.stop = entry.stop
        self.initial_stop = entry.stop
        self.next_index = 0
        self.trail_index = 0


def simulate(
    entries: list[EntrySignal],
    bars_by_tf: dict[str, list[CandleBar]],
    *,
    equity: float = DEFAULT_EQUITY,
    slippage_bps: float = DEFAULT_SLIPPAGE_BPS,
    exit_mode: str = "baseline",
    trails: list[TrailLevel] | None = None,
) -> SimResult:
    rules = EXIT_MODES[exit_mode]
    entries = sorted(entries, key=lambda item: (item.close_time, item.timeframe, item.direction))
    trails = sorted(trails or [], key=lambda item: item.time)
    state: dict[str, _Open | None] = {"pos": None}
    closed: list[PaperTrade] = []
    blocked = 0
    cash = equity

    def _close(position: _Open, price: float, when: datetime, reason: str) -> None:
        nonlocal cash
        exit_fill = _fill(price, position.entry.direction, slippage_bps, entering=False)
        fee_rate = TAKER_FEE.get(position.entry.exchange, 0.001)
        exit_fee = exit_fill * position.size * fee_rate
        sign = 1 if position.entry.direction == "long" else -1
        pnl = position.size * (exit_fill - position.fill) * sign - position.entry_fee - exit_fee
        r_multiple = pnl / position.risk if position.risk else 0.0
        cash += pnl
        closed.append(
            PaperTrade(
                signal_id=position.entry.signal_id,
                exchange=position.entry.exchange,
                symbol=position.entry.symbol,
                timeframe=position.entry.timeframe,
                direction=position.entry.direction,
                opened_at=position.entry.close_time,
                closed_at=when,
                entry=position.fill,
                stop=position.stop,
                exit=exit_fill,
                exit_reason=reason,
                size=position.size,
                pnl=pnl,
                r_multiple=r_multiple,
                fee=position.entry_fee + exit_fee,
                realized=True,
                entry_fee=position.entry_fee,
                variant=exit_mode,
            )
        )

    def _ratchet(position: _Open, bar: CandleBar) -> None:
        if not rules["trail"]:
            return
        while position.trail_index < len(trails):
            level = trails[position.trail_index]
            if level.time > bar.close_time:
                break
            position.trail_index += 1
            if level.direction != position.entry.direction:
                continue
            if level.time <= position.entry.close_time:
                continue
            if position.entry.direction == "long" and position.stop < level.price < bar.close:
                position.stop = level.price
            if position.entry.direction == "short" and bar.close < level.price < position.stop:
                position.stop = level.price

    def _two_close(position: _Open, bars: list[CandleBar], index: int) -> bool:
        if not rules["two_close"] or index < 2:
            return False
        bar, prev, before = bars[index], bars[index - 1], bars[index - 2]
        if prev.close_time <= position.entry.close_time:
            return False
        level = position.entry.level
        if position.entry.direction == "long":
            inside = bar.close < level and prev.close < level
            sequence = bar.low < prev.low and prev.low < before.low
        else:
            inside = bar.close > level and prev.close > level
            sequence = bar.high > prev.high and prev.high > before.high
        return inside and sequence

    def _advance(until: datetime) -> None:
        position = state["pos"]
        if position is None:
            return
        bars = bars_by_tf.get(position.entry.timeframe, [])
        index = position.next_index
        while index < len(bars):
            bar = bars[index]
            if bar.close_time <= position.entry.close_time:
                index += 1
                continue
            if bar.close_time > until:
                break
            _ratchet(position, bar)
            reason = "trail" if position.stop != position.initial_stop else "stop"
            hit = position.entry.direction == "long" and bar.low <= position.stop
            hit = hit or (position.entry.direction == "short" and bar.high >= position.stop)
            if rules["stop"] and hit:
                _close(position, position.stop, bar.close_time, reason)
                state["pos"] = None
                return
            if _two_close(position, bars, index):
                _close(position, bar.close, bar.close_time, "two_lower_closes")
                state["pos"] = None
                return
            index += 1
        if state["pos"] is not None:
            state["pos"].next_index = index

    for entry in entries:
        _advance(entry.close_time)
        position = state["pos"]
        if position is not None:
            if rules["opposite"] and position.entry.direction != entry.direction:
                _close(position, entry.price, entry.close_time, "opposite_signal")
                state["pos"] = None
            else:
                blocked += 1
                continue
        if cash <= 0:
            blocked += 1
            continue
        stop_distance = abs(entry.price - entry.stop)
        risk = cash * RISK_FRACTION
        if stop_distance <= 0 or risk <= 0:
            continue
        fill = _fill(entry.price, entry.direction, slippage_bps, entering=True)
        fee_rate = TAKER_FEE.get(entry.exchange, 0.001)
        size = risk / stop_distance
        state["pos"] = _Open(entry, fill, size, risk, fill * size * fee_rate)

    last_time = max(
        (bar.close_time for bars in bars_by_tf.values() for bar in bars),
        default=None,
    )
    if last_time is not None:
        _advance(last_time)

    still_open: list[PaperTrade] = []
    position = state["pos"]
    if position is not None and last_time is not None:
        bars = bars_by_tf.get(position.entry.timeframe, [])
        mark = bars[-1].close if bars else position.entry.price
        sign = 1 if position.entry.direction == "long" else -1
        pnl = position.size * (mark - position.fill) * sign - position.entry_fee
        still_open.append(
            PaperTrade(
                signal_id=position.entry.signal_id,
                exchange=position.entry.exchange,
                symbol=position.entry.symbol,
                timeframe=position.entry.timeframe,
                direction=position.entry.direction,
                opened_at=position.entry.close_time,
                closed_at=None,
                entry=position.fill,
                stop=position.stop,
                exit=mark,
                exit_reason="open",
                size=position.size,
                pnl=pnl,
                r_multiple=pnl / position.risk if position.risk else 0.0,
                fee=position.entry_fee,
                realized=False,
                entry_fee=position.entry_fee,
                variant=exit_mode,
            )
        )
    return SimResult(trades=closed + still_open, blocked=blocked, equity=cash)
