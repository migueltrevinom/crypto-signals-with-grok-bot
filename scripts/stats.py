"""Window accounting. Win rate and average R use closed trades only."""

import math
from datetime import UTC, datetime

from Repositories.PaperTrading.modules.simulator import DEFAULT_EQUITY, PaperTrade

REGIMES: list[tuple[str, str, str]] = [
    ("2018 bear", "2018-01-01", "2018-12-31"),
    ("2019 recovery", "2019-01-01", "2020-02-29"),
    ("2020 crash", "2020-03-01", "2020-04-30"),
    ("2020-21 bull", "2020-05-01", "2021-11-30"),
    ("2022 bear", "2022-01-01", "2022-12-31"),
    ("2023 recovery", "2023-01-01", "2023-12-31"),
    ("2024 bull", "2024-01-01", "2024-12-31"),
    ("2025-2026", "2025-01-01", "2026-12-31"),
]

IN_SAMPLE = ("2017-2022 in sample", "2017-01-01", "2022-12-31")
OUT_OF_SAMPLE = ("2023-now out of sample", "2023-01-01", "2026-12-31")


def _utc(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=UTC)


def window_bounds(start: str, end: str) -> tuple[datetime, datetime]:
    return _utc(start), _utc(end).replace(hour=23, minute=59)


def in_window(moment: datetime, start: str, end: str) -> bool:
    begin, finish = window_bounds(start, end)
    return begin <= moment <= finish


def _sign(direction: str) -> int:
    return 1 if direction == "long" else -1


def _open_on(trade: PaperTrade, moment: datetime) -> bool:
    if trade.opened_at > moment:
        return False
    return trade.closed_at is None or trade.closed_at > moment


def _mark(trade: PaperTrade, price: float) -> float:
    return trade.size * (price - trade.entry) * _sign(trade.direction) - trade.entry_fee


def equity_curve(
    trades: list[PaperTrade],
    daily: list,
    start: str,
    end: str,
    start_equity: float = DEFAULT_EQUITY,
) -> list[tuple[datetime, float]]:
    begin, finish = window_bounds(start, end)
    days = [bar for bar in daily if begin <= bar.close_time <= finish]
    curve: list[tuple[datetime, float]] = []
    for bar in days:
        realized = sum(
            trade.pnl
            for trade in trades
            if trade.realized and trade.closed_at is not None and trade.closed_at <= bar.close_time
        )
        unrealized = sum(
            _mark(trade, bar.close) for trade in trades if _open_on(trade, bar.close_time)
        )
        curve.append((bar.close_time, start_equity + realized + unrealized))
    return curve


def _ratios(curve: list[tuple[datetime, float]]) -> tuple[float | None, float | None, float | None]:
    if len(curve) < 3:
        return None, None, None
    returns = []
    for previous, current in zip(curve, curve[1:]):
        if previous[1] > 0:
            returns.append(current[1] / previous[1] - 1)
    if len(returns) < 2:
        return None, None, None
    mean = sum(returns) / len(returns)
    var = sum((item - mean) ** 2 for item in returns) / (len(returns) - 1)
    std = math.sqrt(var)
    downside = [min(item, 0.0) for item in returns]
    down_var = sum(item**2 for item in downside) / (len(returns) - 1)
    down_std = math.sqrt(down_var)
    sharpe = mean / std * math.sqrt(365) if std > 0 else None
    sortino = mean / down_std * math.sqrt(365) if down_std > 0 else None
    days = max((curve[-1][0] - curve[0][0]).days, 1)
    cagr = None
    if curve[0][1] > 0 and curve[-1][1] > 0:
        cagr = (curve[-1][1] / curve[0][1]) ** (365 / days) - 1
    return sharpe, sortino, cagr


def buy_and_hold(daily: list, start: str, end: str) -> float | None:
    begin, finish = window_bounds(start, end)
    window = [bar for bar in daily if begin <= bar.close_time <= finish]
    if len(window) < 2 or window[0].close <= 0:
        return None
    return (window[-1].close / window[0].close) - 1


def buy_and_hold_sharpe(daily: list, start: str, end: str) -> float | None:
    begin, finish = window_bounds(start, end)
    window = [bar for bar in daily if begin <= bar.close_time <= finish]
    if len(window) < 3:
        return None
    curve = [(bar.close_time, bar.close) for bar in window]
    sharpe, _sortino, _cagr = _ratios(curve)
    return sharpe


def window_metrics(
    trades: list[PaperTrade],
    daily: list,
    start: str,
    end: str,
    *,
    blocked: int = 0,
    start_equity: float = DEFAULT_EQUITY,
) -> dict:
    begin, finish = window_bounds(start, end)
    closed = [
        trade
        for trade in trades
        if trade.realized and trade.closed_at is not None and begin <= trade.closed_at <= finish
    ]
    curve = equity_curve(trades, daily, start, end, start_equity)
    sharpe, sortino, cagr = _ratios(curve)
    exposed = 0
    for moment, _equity in curve:
        if any(_open_on(trade, moment) for trade in trades):
            exposed += 1
    durations = [
        (trade.closed_at - trade.opened_at).total_seconds() / 86400
        for trade in closed
        if trade.closed_at is not None
    ]
    realized = sum(trade.pnl for trade in closed)
    unrealized = 0.0
    if curve:
        end_price = next(bar.close for bar in reversed(daily) if begin <= bar.close_time <= finish)
        for trade in trades:
            if _open_on(trade, curve[-1][0]):
                unrealized += _mark(trade, end_price)
    total_return = None
    if curve and curve[0][1] > 0:
        total_return = curve[-1][1] / curve[0][1] - 1
    max_dd = None
    if curve:
        peak = curve[0][1]
        max_dd = 0.0
        for _moment, value in curve:
            peak = max(peak, value)
            if peak > 0:
                max_dd = max(max_dd, (peak - value) / peak)
    wins = [trade for trade in closed if trade.r_multiple > 0]
    losses = [trade.pnl for trade in closed if trade.pnl < 0]
    win_pnls = [trade.pnl for trade in closed if trade.pnl > 0]
    profit_factor = None
    if losses:
        profit_factor = (sum(win_pnls) / abs(sum(losses))) if win_pnls else 0.0
    elif win_pnls:
        profit_factor = float("inf")
    return {
        "closed": len(closed),
        "blocked": blocked,
        "win_rate": (len(wins) / len(closed)) if closed else None,
        "avg_r": (sum(trade.r_multiple for trade in closed) / len(closed)) if closed else None,
        "expectancy": (sum(trade.r_multiple for trade in closed) / len(closed)) if closed else None,
        "profit_factor": profit_factor,
        "max_dd": max_dd,
        "realized": realized,
        "unrealized": unrealized,
        "return": total_return,
        "sharpe": sharpe,
        "sortino": sortino,
        "cagr": cagr,
        "exposure": (exposed / len(curve)) if curve else None,
        "avg_days": (sum(durations) / len(durations)) if durations else None,
        "buy_hold": buy_and_hold(daily, start, end),
        "buy_hold_sharpe": buy_and_hold_sharpe(daily, start, end),
    }


def fmt_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    if value == float("inf"):
        return "inf"
    return f"{value * 100:.1f}%"


def fmt_num(value: float | None) -> str:
    if value is None:
        return "n/a"
    if value == float("inf"):
        return "inf"
    return f"{value:.2f}"


def _series_ratios(returns: list[float], days: int, start_value: float, end_value: float) -> dict:
    if len(returns) < 2 or days < 1:
        return {"sharpe": None, "sortino": None, "cagr": None, "return": None}
    mean = sum(returns) / len(returns)
    var = sum((item - mean) ** 2 for item in returns) / (len(returns) - 1)
    std = math.sqrt(var)
    downside = [min(item, 0.0) for item in returns]
    down_std = math.sqrt(sum(item**2 for item in downside) / (len(returns) - 1))
    total = None
    if start_value > 0 and end_value > 0:
        total = end_value / start_value - 1
    cagr = None
    if start_value > 0 and end_value > 0:
        cagr = (end_value / start_value) ** (365 / days) - 1
    return {
        "sharpe": (mean / std * math.sqrt(365)) if std > 0 else None,
        "sortino": (mean / down_std * math.sqrt(365)) if down_std > 0 else None,
        "cagr": cagr,
        "return": total,
    }


def portfolio_metrics(
    sleeves: list[tuple[list[PaperTrade], list]],
    start: str,
    end: str,
) -> dict:
    """Equal-weight daily returns of every sleeve that has a bar that day."""
    strategy: dict[datetime, list[float]] = {}
    holds: dict[datetime, list[float]] = {}
    begin, finish = window_bounds(start, end)
    for trades, daily in sleeves:
        curve = equity_curve(trades, daily, start, end)
        for previous, current in zip(curve, curve[1:]):
            if previous[1] > 0:
                strategy.setdefault(current[0], []).append(current[1] / previous[1] - 1)
        window = [bar for bar in daily if begin <= bar.close_time <= finish]
        for previous, current in zip(window, window[1:]):
            if previous.close > 0:
                holds.setdefault(current.close_time, []).append(current.close / previous.close - 1)
    strat_days = sorted(strategy)
    hold_days = sorted(holds)
    strat_returns = [sum(strategy[day]) / len(strategy[day]) for day in strat_days]
    hold_returns = [sum(holds[day]) / len(holds[day]) for day in hold_days]
    strat_equity = 1.0
    for item in strat_returns:
        strat_equity *= 1 + item
    hold_equity = 1.0
    for item in hold_returns:
        hold_equity *= 1 + item
    span = (strat_days[-1] - strat_days[0]).days if len(strat_days) > 1 else 0
    hold_span = (hold_days[-1] - hold_days[0]).days if len(hold_days) > 1 else 0
    stats = _series_ratios(strat_returns, span, 1.0, strat_equity)
    bench = _series_ratios(hold_returns, hold_span, 1.0, hold_equity)
    stats["bh_sharpe"] = bench["sharpe"]
    stats["bh_sortino"] = bench["sortino"]
    stats["bh_cagr"] = bench["cagr"]
    stats["bh_return"] = bench["return"]
    stats["pairs"] = len(sleeves)
    return stats


def beats_buy_hold(stats: dict) -> bool:
    sharpe = stats.get("sharpe")
    bench = stats.get("buy_hold_sharpe")
    if sharpe is None or bench is None:
        return False
    return sharpe > bench
