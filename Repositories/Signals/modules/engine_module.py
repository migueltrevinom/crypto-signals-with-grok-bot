"""time@mode entries for one symbol.

Detection is the ported prototype. The 6h SMA filter, the ladder, and the
confluence score are the decisions in docs/strategy-spec.md. Parameters are
not optimized here. Swing signals are stamped on the confirming bar, which
is what detect_modes already does.
"""

import subprocess
from dataclasses import dataclass
from datetime import datetime

import numpy as np

from Core.config import REPO_ROOT
from Core.planning_seeds import CONFLUENCE_SEED
from Core.prototype_config import load_prototype_config
from Repositories.MarketData.modules.candles import CandleBar, ms
from Repositories.PaperTrading.modules.simulator import EntrySignal, TrailLevel, protective_stop
from Repositories.Performance.modules.hashchain import signal_key
from Repositories.Strategies.TimeMode.helpers import timemode as tm

ENTRY_TFS = ("4h", "6h", "8h")
DECISION_TFS = ("1w", "3d", "1d")
LADDER = ("4h", "6h", "8h", "1d", "3d", "1w", "1M")
THRESHOLD = float(CONFLUENCE_SEED["thresholds"]["entry"])
WEIGHTS = CONFLUENCE_SEED["weights"]


def detection_params() -> dict:
    params = dict(load_prototype_config()["params"])
    params["sma_filter_timeframe"] = "6h"
    return params


def strategy_version(params: dict) -> str:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        sha = "unknown"
    return f"{sha}:atr{params.get('confirm_atr_mult')}"


@dataclass
class _Event:
    type: str
    direction: str
    timeframe: str
    htf: str | None
    close_time: datetime
    expiry_time: datetime | None
    price: float
    level: float
    atr: float
    length: int
    low: float
    high: float
    block_low: float | None = None
    block_high: float | None = None


def _dir_name(value: int, kind: str) -> str:
    if kind in {"block_breakout_entry", "exit"}:
        return "long" if value > 0 else "short"
    return "bullish" if value > 0 else "bearish"


def _same(direction: str, other: str) -> bool:
    bull = direction in {"long", "bullish"}
    other_bull = other in {"long", "bullish"}
    return bull == other_bull


def _arrays(bars: list[CandleBar]) -> dict:
    rows = [bar.as_dict() for bar in bars]
    return tm.arrays(rows)


def _modes(bars: list[CandleBar], timeframe: str, params: dict) -> list[_Event]:
    if len(bars) < 80:
        return []
    data = _arrays(bars)
    events: list[_Event] = []
    for sig in tm.detect_modes(data, tm.params_for(params, timeframe)):
        if sig["type"] != "mode_confirmed":
            continue
        close_at = bars[sig["bar"]].close_time
        expiry_at = bars[min(sig["expiry_bar"], len(bars) - 1)].close_time
        events.append(
            _Event(
                type="mode_confirmed",
                direction=_dir_name(sig["dir"], "mode_confirmed"),
                timeframe=timeframe,
                htf=None,
                close_time=close_at,
                expiry_time=expiry_at,
                price=float(sig["price"]),
                level=float(sig["level"]),
                atr=float(sig["atr"]),
                length=int(sig["length"]),
                low=float(bars[sig["bar"]].low),
                high=float(bars[sig["bar"]].high),
            )
        )
    return events


def _blocks(
    htf_bars: list[CandleBar],
    ltf_bars: list[CandleBar],
    htf: str,
    ltf: str,
    params: dict,
    sma_6h: tuple[np.ndarray, np.ndarray],
) -> list[_Event]:
    if len(htf_bars) < 40 or len(ltf_bars) < 80:
        return []
    high = _arrays(htf_bars)
    low = _arrays(ltf_bars)
    events: list[_Event] = []
    for sig in tm.detect_blocks(high, low, tm.params_for(params, ltf), sma_6h):
        if sig["type"] != "block_breakout_entry":
            continue
        bar = ltf_bars[sig["bar"]]
        block_index = int(sig["htf_block_bar"])
        block_low = block_high = None
        if 0 <= block_index < len(htf_bars):
            block_low = float(htf_bars[block_index].low)
            block_high = float(htf_bars[block_index].high)
        events.append(
            _Event(
                type="block_breakout_entry",
                direction=_dir_name(sig["dir"], "block_breakout_entry"),
                timeframe=ltf,
                htf=htf,
                close_time=bar.close_time,
                expiry_time=None,
                price=float(sig["price"]),
                level=float(sig["level"]),
                atr=float(sig["atr"]),
                length=0,
                low=float(bar.low),
                high=float(bar.high),
                block_low=block_low,
                block_high=block_high,
            )
        )
    return events


def _sma_series(bars_6h: list[CandleBar], length: int) -> tuple[np.ndarray, np.ndarray]:
    if len(bars_6h) < length + 2:
        return np.array([]), np.array([])
    data = _arrays(bars_6h)
    values = tm.sma(data["c"], length)
    return data["ct"].astype(np.int64), values


def prepare(
    exchange: str,
    symbol: str,
    series: dict[str, list[CandleBar]],
    *,
    params: dict | None = None,
    window_start: datetime | None = None,
    require_sma: bool = True,
    min_decision_tfs: int = 1,
    with_trails: bool = True,
) -> tuple[list[EntrySignal], list[TrailLevel]]:
    """Causal entries. `window_start` keeps live scans to recent bars."""
    params = params or detection_params()
    version = strategy_version(params)
    modes: list[_Event] = []
    for timeframe in LADDER:
        modes.extend(_modes(series.get(timeframe, []), timeframe, params))
    times, values = _sma_series(series.get("6h", []), int(params["sma_length"]))
    blocks: list[_Event] = []
    for htf in DECISION_TFS:
        for ltf in ENTRY_TFS:
            blocks.extend(
                _blocks(series.get(htf, []), series.get(ltf, []), htf, ltf, params, (times, values))
            )
    swings = _swing_index(series, int(params.get("swing_lookback", 5)))
    candidates = [
        item
        for item in modes + blocks
        if item.timeframe in ENTRY_TFS
        and (window_start is None or item.close_time >= window_start)
    ]
    candidates.sort(key=lambda item: item.close_time)
    chosen: dict[tuple, EntrySignal] = {}
    for candidate in candidates:
        side, sma_value = _sma_ok(times, values, candidate)
        sma_pass = side in {"above", "below"}
        if require_sma and not sma_pass:
            continue
        score, hits = _score(candidate, modes, blocks, side if sma_pass else "")
        decision = sorted({item.split(":", 1)[1] for item in hits if ":" in item})
        if score < THRESHOLD or len(decision) < min_decision_tfs:
            continue
        direction = "long" if candidate.direction in {"long", "bullish"} else "short"
        extreme = candidate.low if direction == "long" else candidate.high
        stop = protective_stop(direction, candidate.price, candidate.level, extreme, candidate.atr)
        close_ms = ms(candidate.close_time)
        signal_id = signal_key(
            exchange=exchange,
            symbol=symbol,
            timeframe=candidate.timeframe,
            direction=direction,
            close_ms=close_ms,
            level=candidate.level,
        )
        key = (direction, candidate.close_time, candidate.timeframe)
        current = chosen.get(key)
        if current is not None and current.score >= score:
            continue
        chosen[key] = EntrySignal(
            exchange=exchange,
            symbol=symbol,
            timeframe=candidate.timeframe,
            direction=direction,
            close_time=candidate.close_time,
            price=candidate.price,
            level=candidate.level,
            atr=candidate.atr,
            stop=stop,
            score=score,
            signal_id=signal_id,
            candle_low=candidate.low,
            candle_high=candidate.high,
            strategy_version=version,
            inputs={
                "level": candidate.level,
                "atr": candidate.atr,
                "sma_6h": sma_value,
                "score": score,
                "decision_hits": hits,
                "trigger": candidate.type,
                "htf": candidate.htf,
                "ohlcv_hash": None,
                "sma_pass": sma_pass,
                "decision_tfs": decision,
                "wick": _mode_wick(candidate, modes),
                "block": _block_extreme(candidate, blocks),
                "swing": _last_swing(swings, candidate.timeframe, direction, candidate.close_time),
            },
        )
    entries = sorted(chosen.values(), key=lambda item: item.close_time)
    trails = _trail_levels(series, modes, params) if with_trails else []
    return entries, trails


def _swing_index(
    series: dict[str, list[CandleBar]], lookback: int
) -> dict[str, dict[str, list[tuple[datetime, float]]]]:
    indexed: dict[str, dict[str, list[tuple[datetime, float]]]] = {}
    for timeframe, bars in series.items():
        if len(bars) < lookback * 2 + 2:
            continue
        data = _arrays(bars)
        highs, lows = tm.swings(data["h"], data["l"], lookback)
        indexed[timeframe] = {
            "long": [
                (bars[index + lookback].close_time, float(data["l"][index]))
                for index in lows
                if index + lookback < len(bars)
            ],
            "short": [
                (bars[index + lookback].close_time, float(data["h"][index]))
                for index in highs
                if index + lookback < len(bars)
            ],
        }
    return indexed


def _last_swing(
    indexed: dict[str, dict[str, list[tuple[datetime, float]]]],
    timeframe: str,
    direction: str,
    when: datetime,
) -> float | None:
    rows = indexed.get(timeframe, {}).get(direction, [])
    lo, hi = 0, len(rows)
    while lo < hi:
        mid = (lo + hi) // 2
        if rows[mid][0] <= when:
            lo = mid + 1
        else:
            hi = mid
    if lo == 0:
        return None
    return rows[lo - 1][1]


def _mode_wick(candidate: _Event, modes: list[_Event]) -> float | None:
    if candidate.type == "mode_confirmed":
        return candidate.level
    best: _Event | None = None
    for mode in modes:
        if mode.timeframe != candidate.timeframe or mode.close_time > candidate.close_time:
            continue
        if mode.expiry_time is not None and mode.expiry_time < candidate.close_time:
            continue
        if not _same(mode.direction, candidate.direction):
            continue
        if best is None or mode.close_time >= best.close_time:
            best = mode
    return None if best is None else best.level


def _block_extreme(candidate: _Event, blocks: list[_Event]) -> float | None:
    long = candidate.direction in {"long", "bullish"}
    if candidate.block_low is not None and candidate.block_high is not None:
        return candidate.block_low if long else candidate.block_high
    best: _Event | None = None
    for block in blocks:
        if block.close_time > candidate.close_time or block.block_low is None:
            continue
        if not _same(block.direction, candidate.direction):
            continue
        if best is None or block.close_time >= best.close_time:
            best = block
    if best is None or best.block_low is None or best.block_high is None:
        return None
    return best.block_low if long else best.block_high


def build_entries(
    exchange: str,
    symbol: str,
    series: dict[str, list[CandleBar]],
    *,
    params: dict | None = None,
    window_start: datetime | None = None,
) -> list[EntrySignal]:
    return prepare(
        exchange, symbol, series, params=params, window_start=window_start
    )[0]


def _trail_levels(
    series: dict[str, list[CandleBar]], modes: list[_Event], params: dict
) -> list[TrailLevel]:
    """Stops from confirmed 5-bar swings and new blocks, only on the TF in control."""
    levels: list[TrailLevel] = []
    lookback = int(params.get("swing_lookback", 5))
    for timeframe, bars in series.items():
        if len(bars) < lookback * 2 + 5:
            continue
        data = _arrays(bars)
        highs, lows = tm.swings(data["h"], data["l"], lookback)
        for index in lows:
            confirm = index + lookback
            if confirm >= len(bars):
                continue
            when = bars[confirm].close_time
            if _timeframe_in_control(modes, when) != timeframe:
                continue
            levels.append(TrailLevel(when, float(data["l"][index]), "long", "swing"))
        for index in highs:
            confirm = index + lookback
            if confirm >= len(bars):
                continue
            when = bars[confirm].close_time
            if _timeframe_in_control(modes, when) != timeframe:
                continue
            levels.append(TrailLevel(when, float(data["h"][index]), "short", "swing"))
        active = tm.htf_blocks(data, tm.params_for(params, timeframe))
        seen: set[tuple] = set()
        for bar_index, rows in active.items():
            when = bars[bar_index].close_time
            if _timeframe_in_control(modes, when) != timeframe:
                continue
            for direction, level, block_bar in rows:
                key = (timeframe, direction, block_bar)
                if key in seen:
                    continue
                seen.add(key)
                side = "long" if direction > 0 else "short"
                levels.append(TrailLevel(when, float(level), side, "block"))
    levels.sort(key=lambda item: item.time)
    return levels


def _sma_ok(
    times: np.ndarray, values: np.ndarray, event: _Event
) -> tuple[str | None, float]:
    if len(times) == 0:
        return None, 0.0
    when = ms(event.close_time)
    index = int(np.searchsorted(times, when, side="right") - 1)
    if index < 0 or np.isnan(values[index]):
        return None, 0.0
    sma_value = float(values[index])
    # The 6h close that owns this SMA is the bar whose close time is times[index].
    # Price vs SMA uses the entry close. Longs must be above the 6h SMA.
    bullish = event.direction in {"long", "bullish"}
    if bullish and event.price <= sma_value:
        return None, sma_value
    if not bullish and event.price >= sma_value:
        return None, sma_value
    return ("above" if bullish else "below"), sma_value


def _score(
    candidate: _Event,
    modes: list[_Event],
    blocks: list[_Event],
    sma_side: str,
) -> tuple[float, list[str]]:
    when = candidate.close_time
    score = WEIGHTS["sma_6h_agreement"] if sma_side else 0.0
    hits: list[str] = []
    directions_by_tf: dict[str, set[str]] = {}
    latest_mode: dict[str, _Event] = {}
    for mode in modes:
        if mode.close_time > when:
            continue
        if mode.expiry_time is not None and mode.expiry_time < when:
            continue
        if mode.length < 5 or mode.length > 20:
            continue
        directions_by_tf.setdefault(mode.timeframe, set()).add(mode.direction)
        previous = latest_mode.get(mode.timeframe)
        if previous is None or mode.close_time >= previous.close_time:
            latest_mode[mode.timeframe] = mode
    for timeframe, mode in latest_mode.items():
        if _same(mode.direction, candidate.direction):
            score += WEIGHTS["mode_confirmed"].get(timeframe, 0)
            if timeframe in DECISION_TFS:
                hits.append(f"mode:{timeframe}")
    latest_block: dict[str, _Event] = {}
    for block in blocks:
        if block.close_time > when or block.htf is None:
            continue
        previous = latest_block.get(block.htf)
        if previous is None or block.close_time >= previous.close_time:
            latest_block[block.htf] = block
    for htf, block in latest_block.items():
        if _same(block.direction, candidate.direction):
            score += WEIGHTS["block_break"].get(htf, 0)
            if htf in DECISION_TFS:
                hits.append(f"block:{htf}")
    tfc = _timeframe_in_control(modes, when)
    if tfc is not None:
        active = [
            mode
            for mode in modes
            if mode.timeframe == tfc
            and mode.close_time <= when
            and (mode.expiry_time is None or mode.expiry_time >= when)
        ]
        if any(_same(mode.direction, candidate.direction) for mode in active):
            score += WEIGHTS["timeframe_in_control_agreement"]
    opposed = False
    for timeframe in DECISION_TFS:
        dirs = directions_by_tf.get(timeframe, set())
        if any(not _same(item, candidate.direction) for item in dirs) and any(
            _same(item, candidate.direction) for item in dirs
        ):
            opposed = True
    if opposed:
        score -= WEIGHTS["htf_conflict_penalty"]
    return score, sorted(set(hits))


def _timeframe_in_control(modes: list[_Event], when: datetime) -> str | None:
    for timeframe in LADDER:
        fit = [
            mode
            for mode in modes
            if mode.timeframe == timeframe
            and mode.close_time <= when
            and mode.expiry_time is not None
            and mode.expiry_time >= when
            and 5 <= mode.length <= 20
        ]
        if fit:
            return timeframe
    return "1M"
