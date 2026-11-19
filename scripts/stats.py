"""Trade statistics. R is net of fees and slippage, divided by the 1% risk."""

from datetime import UTC, datetime

from Repositories.PaperTrading.modules.simulator import PaperTrade

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


def in_window(moment: datetime, start: str, end: str) -> bool:
    return _utc(start) <= moment <= _utc(end).replace(hour=23, minute=59)


def buy_and_hold(daily: list, start: str, end: str) -> float | None:
    window = [bar for bar in daily if in_window(bar.close_time, start, end)]
    if len(window) < 2 or window[0].close <= 0:
        return None
    return (window[-1].close / window[0].close) - 1


def summarize(trades: list[PaperTrade], start_equity: float = 10_000.0) -> dict:
    if not trades:
        return {
            "trades": 0,
            "win_rate": None,
            "avg_r": None,
            "expectancy": None,
            "profit_factor": None,
            "max_dd": None,
            "return": None,
        }
    wins = [trade.pnl for trade in trades if trade.pnl > 0]
    losses = [trade.pnl for trade in trades if trade.pnl < 0]
    equity = start_equity
    peak = equity
    max_dd = 0.0
    for trade in trades:
        equity += trade.pnl
        peak = max(peak, equity)
        if peak > 0:
            max_dd = max(max_dd, (peak - equity) / peak)
    profit_factor = None
    if losses:
        profit_factor = sum(wins) / abs(sum(losses)) if wins else 0.0
    elif wins:
        profit_factor = float("inf")
    avg_r = sum(trade.r_multiple for trade in trades) / len(trades)
    return {
        "trades": len(trades),
        "win_rate": sum(1 for trade in trades if trade.r_multiple > 0) / len(trades),
        "avg_r": avg_r,
        "expectancy": avg_r,
        "profit_factor": profit_factor,
        "max_dd": max_dd,
        "return": (equity / start_equity) - 1,
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
