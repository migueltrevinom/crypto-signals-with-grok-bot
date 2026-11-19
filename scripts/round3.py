"""Stop placement and filter ablations on the opposite-signal exit.

72 discrete variants. No threshold search. No live orders.
Writes reports/round3.md and reports/portfolio_equity.png.
"""

import asyncio
import csv
import json
import sys
from collections import Counter
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from Core.config import REPO_ROOT
from Repositories.PaperTrading.modules.simulator import simulate, stop_beyond
from Repositories.Signals.modules.engine_module import prepare
from scripts.history import CACHE, get_series
from scripts.stats import (
    IN_SAMPLE,
    OUT_OF_SAMPLE,
    equity_curve,
    fmt_num,
    fmt_pct,
    portfolio_metrics,
    window_bounds,
)

EXCHANGES = ("binance", "kucoin")
SYMBOLS = (
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "ARBUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "LINKUSDT",
)
HISTORY_START = datetime(2017, 1, 1, tzinfo=UTC)
REPORTS = REPO_ROOT / "reports"
INTERVAL_MS = {"4h": 14_400_000, "6h": 21_600_000, "8h": 28_800_000}
ANCHORS = ("wick", "block", "swing")
BUFFERS = (0.25, 1.0, 2.0)


class Spec:
    def __init__(
        self, anchor: str, buffer: float, sma: bool, directions: tuple[str, ...], confluence: int
    ) -> None:
        self.anchor = anchor
        self.buffer = buffer
        self.sma = sma
        self.directions = directions
        self.confluence = confluence

    def label(self) -> str:
        sma = "SMA on" if self.sma else "SMA off"
        side = "long+short" if len(self.directions) == 2 else "long only"
        return f"{self.anchor} / {self.buffer:.2f} ATR / {sma} / {side} / {self.confluence} of 3"


def grid() -> list[Spec]:
    specs = []
    for anchor in ANCHORS:
        for buffer in BUFFERS:
            for sma in (True, False):
                for directions in (("long", "short"), ("long",)):
                    for confluence in (1, 2):
                        specs.append(Spec(anchor, buffer, sma, directions, confluence))
    return specs


def select(entries: list, spec: Spec) -> list:
    chosen = []
    for entry in entries:
        if spec.sma and not entry.inputs.get("sma_pass"):
            continue
        if entry.direction not in spec.directions:
            continue
        if len(entry.inputs.get("decision_tfs", [])) < spec.confluence:
            continue
        chosen.append(entry)
    return chosen


def place(entries: list, spec: Spec) -> tuple[list, int]:
    placed = []
    skipped = 0
    for entry in entries:
        anchor = entry.inputs.get(spec.anchor)
        if anchor is None:
            skipped += 1
            continue
        stop = stop_beyond(entry.direction, entry.price, float(anchor), entry.atr, spec.buffer)
        if stop is None:
            skipped += 1
            continue
        placed.append(replace(entry, stop=stop))
    return placed, skipped


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def closed_stats(trades: list, start: str | None = None, end: str | None = None) -> dict:
    if start and end:
        begin, finish = window_bounds(start, end)
        closed = [
            trade
            for trade in trades
            if trade.realized and trade.closed_at is not None and begin <= trade.closed_at <= finish
        ]
    else:
        closed = [trade for trade in trades if trade.realized and trade.closed_at is not None]
    wins = [trade.r_multiple for trade in closed if trade.r_multiple > 0]
    losses = [trade.r_multiple for trade in closed if trade.r_multiple <= 0]
    durations = [
        (trade.closed_at - trade.opened_at).total_seconds() / 86400
        for trade in closed
        if trade.closed_at is not None
    ]
    reasons = Counter(trade.exit_reason for trade in closed)
    return {
        "closed": len(closed),
        "win_rate": (len(wins) / len(closed)) if closed else None,
        "avg_win_r": _mean(wins),
        "avg_loss_r": _mean(losses),
        "expectancy": _mean([trade.r_multiple for trade in closed]),
        "avg_days": _mean(durations),
        "reasons": reasons,
    }


def pooled_stats(sleeves: list[tuple[list, list]], start: str, end: str) -> dict:
    trades = [trade for sleeve, _daily in sleeves for trade in sleeve]
    return closed_stats(trades, start, end)


def compound(sleeves: list[tuple[list, list]], start: str, end: str) -> list[tuple[datetime, float]]:  # noqa: E501
    grouped: dict[datetime, list[float]] = {}
    for trades, daily in sleeves:
        curve = equity_curve(trades, daily, start, end)
        for previous, current in zip(curve, curve[1:]):
            if previous[1] > 0:
                grouped.setdefault(current[0], []).append(current[1] / previous[1] - 1)
    equity = 1.0
    points = []
    for day in sorted(grouped):
        returns = grouped[day]
        equity *= 1 + sum(returns) / len(returns)
        points.append((day, equity))
    return points


def buy_hold_curve(
    sleeves: list[tuple[list, list]], start: str, end: str
) -> list[tuple[datetime, float]]:
    begin, finish = window_bounds(start, end)
    grouped: dict[datetime, list[float]] = {}
    for _trades, daily in sleeves:
        window = [bar for bar in daily if begin <= bar.close_time <= finish]
        for previous, current in zip(window, window[1:]):
            if previous.close > 0:
                change = current.close / previous.close - 1
                grouped.setdefault(current.close_time, []).append(change)
    equity = 1.0
    points = []
    for day in sorted(grouped):
        returns = grouped[day]
        equity *= 1 + sum(returns) / len(returns)
        points.append((day, equity))
    return points


def _reason_text(reasons: Counter) -> str:
    return ", ".join(f"{key} {value}" for key, value in sorted(reasons.items()))


def diagnose_published_baseline() -> list[str]:
    """The cited 0% win rate is the round-2 baseline, read from the committed CSVs."""
    lines = [
        "## Why baseline closed trades win about 0%",
        "",
        "The cited Binance BTC cell is the round-2 baseline (fixed stop or two closes,",
        "one position per direction). A stop beyond the entry can only book a loss,",
        "and the two-close rule fires after price is back inside the broken level,",
        "which is also a loss after fees. Trades that never hit either rule stay open",
        "and are left out of the closed-trade win rate.",
        "",
    ]
    begin, finish = window_bounds(IN_SAMPLE[1], IN_SAMPLE[2])
    btc_in = []
    all_stops = wick = through = missing = 0
    fast = 0
    for path in sorted(REPORTS.glob("trades-*-*.csv")):
        exchange, symbol = path.stem.split("-")[1:3]
        with path.open(encoding="utf-8") as handle:
            rows = [
                row
                for row in csv.DictReader(handle)
                if row["variant"] == "baseline" and row["realized"] == "True"
            ]
        caches = {
            timeframe: _cache_index(exchange, symbol, timeframe) for timeframe in INTERVAL_MS
        }
        for row in rows:
            closed_at = datetime.fromisoformat(row["closed_at"])
            if exchange == "binance" and symbol == "BTCUSDT" and begin <= closed_at <= finish:
                btc_in.append(row)
            if row["exit_reason"] != "stop":
                continue
            all_stops += 1
            bar = caches[row["timeframe"]].get(_ms(closed_at))
            if bar is None:
                missing += 1
                continue
            stop = float(row["stop"])
            recovered = bar["c"] > stop if row["direction"] == "long" else bar["c"] < stop
            if recovered:
                wick += 1
            else:
                through += 1
            opened = datetime.fromisoformat(row["opened_at"])
            if (closed_at - opened).total_seconds() <= 24 * 3600:
                fast += 1
    wins = [row for row in btc_in if float(row["r_multiple"]) > 0]
    reasons = Counter(row["exit_reason"] for row in btc_in)
    rs = [float(row["r_multiple"]) for row in btc_in]
    stops = [row for row in btc_in if row["exit_reason"] == "stop"]
    hours = []
    for row in stops:
        opened = datetime.fromisoformat(row["opened_at"])
        closed_at = datetime.fromisoformat(row["closed_at"])
        hours.append((closed_at - opened).total_seconds() / 3600)
    hours.sort()
    median = hours[len(hours) // 2] if hours else None
    within = sum(item <= 24 for item in hours)
    lines.append(
        f"Binance BTC, closes in 2017-2022: {len(btc_in)} closed, {len(wins)} wins, "
        f"average R {fmt_num(_mean(rs))}. Exits: {_reason_text(reasons)}."
    )
    lines.append(
        f"Of those stop exits, the median hold is {fmt_num(median)} hours and "
        f"{within} of {len(stops)} close within 24 hours."
    )
    lines.append(
        f"Across every baseline stop exit in the round-2 files, {wick} of {all_stops} "
        f"were wick-only (the bar's close finished back beyond the stop), {through} closed "
        f"through the stop, and {missing} had no cached bar. {fast} of {all_stops} closed "
        "within 24 hours."
    )
    lines.append(
        "The 0.25 ATR buffer is tight enough to turn wicks into losses, and it is not the "
        "whole reason the closed-trade win rate is zero: every stop exit is a loss by "
        "construction, and the two-close exits in this cell were losses too."
    )
    lines.append("")
    return lines


def _ms(moment: datetime) -> int:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return int(moment.timestamp() * 1000)


def _cache_index(exchange: str, symbol: str, timeframe: str) -> dict[int, dict]:
    path = CACHE / exchange / symbol / f"{timeframe}.json"
    if not path.exists():
        return {}
    rows = json.loads(path.read_text(encoding="utf-8"))
    step = INTERVAL_MS[timeframe]
    return {int(row["open_ms"]) + step: row for row in rows}


def draw(curves: list[tuple[str, list[tuple[datetime, float]]]], path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    for label, points in curves:
        if not points:
            continue
        xs = [item[0] for item in points]
        ys = [item[1] for item in points]
        ax.plot(xs, ys, label=label, linewidth=1.4)
    ax.axvline(datetime(2023, 1, 1, tzinfo=UTC), color="0.4", linestyle="--", linewidth=1)
    ax.set_yscale("log")
    ax.set_title("Equal-weight portfolio equity, log scale")
    ax.set_ylabel("Growth of 1")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(frameon=False)
    ax.grid(True, which="both", axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


async def run() -> None:
    specs = grid()
    sleeves: dict[str, list] = {spec.label(): [] for spec in specs}
    skipped: dict[str, int] = {spec.label(): 0 for spec in specs}
    published: list = []
    fresh_baseline: list = []
    pair_lines = []
    coverage = {anchor: [0, 0] for anchor in ANCHORS}
    for exchange in EXCHANGES:
        for symbol in SYMBOLS:
            print(f"[prepare] {exchange} {symbol}", file=sys.stderr)
            series = await get_series(exchange, symbol, HISTORY_START)
            if len(series.get("1d", [])) < 80 or len(series.get("6h", [])) < 80:
                print(f"[skip] {exchange} {symbol}", file=sys.stderr)
                continue
            entries, _trails = prepare(
                exchange,
                symbol,
                series,
                require_sma=False,
                min_decision_tfs=1,
                with_trails=False,
            )
            daily = series.get("1d", [])
            reference_entries = select(entries, Spec("wick", 0.25, True, ("long", "short"), 1))
            for anchor in ANCHORS:
                for entry in reference_entries:
                    coverage[anchor][1] += 1
                    if entry.inputs.get(anchor) is not None:
                        coverage[anchor][0] += 1
            published_result = simulate(reference_entries, series, exit_mode="opposite")
            published.append((published_result.trades, daily))
            baseline_result = simulate(reference_entries, series, exit_mode="baseline")
            fresh_baseline.append((baseline_result.trades, daily))
            stats = closed_stats(published_result.trades)
            pair_lines.append(
                f"| {exchange} {symbol} | {stats['closed']} | {fmt_pct(stats['win_rate'])} | "
                f"{fmt_num(stats['avg_win_r'])} | {fmt_num(stats['avg_loss_r'])} | "
                f"{fmt_num(stats['expectancy'])} | {_reason_text(stats['reasons'])} | "
                f"{fmt_num(stats['avg_days'])} |"
            )
            print(
                f"[pair] {exchange} {symbol} signals={len(entries)} "
                f"opposite closed={stats['closed']} blocked={published_result.blocked}",
                file=sys.stderr,
            )
            for spec in specs:
                chosen, missed = place(select(entries, spec), spec)
                skipped[spec.label()] += missed
                result = simulate(chosen, series, exit_mode="opposite")
                sleeves[spec.label()].append((result.trades, daily))
    rows = []
    for spec in specs:
        label = spec.label()
        sample = {
            "in": portfolio_metrics(sleeves[label], IN_SAMPLE[1], IN_SAMPLE[2]),
            "out": portfolio_metrics(sleeves[label], OUT_OF_SAMPLE[1], OUT_OF_SAMPLE[2]),
        }
        pooled = pooled_stats(sleeves[label], OUT_OF_SAMPLE[1], OUT_OF_SAMPLE[2])
        rows.append((spec, sample, pooled, skipped[label]))
    reference = {
        "in": portfolio_metrics(published, IN_SAMPLE[1], IN_SAMPLE[2]),
        "out": portfolio_metrics(published, OUT_OF_SAMPLE[1], OUT_OF_SAMPLE[2]),
    }
    reference_pool = pooled_stats(published, OUT_OF_SAMPLE[1], OUT_OF_SAMPLE[2])
    baseline_pool = pooled_stats(fresh_baseline, IN_SAMPLE[1], IN_SAMPLE[2])

    def beats(sample: dict, side: str) -> bool:
        stats = sample[side]
        return (
            stats["sharpe"] is not None
            and stats["bh_sharpe"] is not None
            and stats["sharpe"] > stats["bh_sharpe"]
        )

    def flag(sample: dict) -> str:
        if beats(sample, "in") and not beats(sample, "out"):
            return "IS only"
        if beats(sample, "out"):
            return "beats OOS"
        return ""

    rows.sort(
        key=lambda item: (
            item[1]["out"]["sharpe"] is not None,
            item[1]["out"]["sharpe"] or -999,
        ),
        reverse=True,
    )
    oos_winners = [item for item in rows if beats(item[1], "out")]
    is_only = [item for item in rows if flag(item[1]) == "IS only"]
    best = rows[0]
    text = _report(
        rows,
        reference,
        reference_pool,
        baseline_pool,
        pair_lines,
        coverage,
        oos_winners,
        is_only,
        best,
        published,
        sleeves[best[0].label()],
    )
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "round3.md").write_text(text, encoding="utf-8")
    print(text.split("## Ranked")[0])


def _report(
    rows,
    reference,
    reference_pool,
    baseline_pool,
    pair_lines,
    coverage,
    oos_winners,
    is_only,
    best,
    published,
    best_sleeves,
) -> str:
    lines = [
        "# Round 3",
        "",
        "Opposite-signal exit, one position per pair. Fees 0.1% per side, slippage 5 bps,",
        "starting equity 10,000. Sharpe and Sortino use equal-weight daily returns of the",
        "20 series (10 USDT symbols on Binance and KuCoin), risk free rate 0, 365-day year.",
        "Win rate and average R use closed trades only.",
        "",
        f"Variants tried in this grid: {len(rows)}. That is 3 stop anchors (mode wick,",
        "trading-block low/high, last confirmed 5-bar swing) × 3 ATR buffers (0.25, 1.0, 2.0)",
        "× SMA filter on or off × long-only or long+short × confluence 1 or 2 of 1w/3d/1d.",
        "The published stop from round 2 is reported separately and is not one of the 72.",
        "Picking the best of 72 out-of-sample Sharpes biases that number upward.",
        "",
    ]
    ref_out = reference["out"]
    best_out = best[1]["out"]
    if beats_sample(ref_out) or oos_winners:
        names = ["published opposite"] if beats_sample(ref_out) else []
        names.extend(item[0].label() for item in oos_winners)
        lines.append(
            "Out of sample, these beat equal-weight buy-and-hold Sharpe: " + "; ".join(names) + "."
        )
    else:
        lines.append(
            "Out of sample, none of the 72 and not the published opposite "
            "beat buy-and-hold Sharpe."
        )
    lines.append(
        f"Published opposite out of sample: return {fmt_pct(ref_out['return'])}, "
        f"Sharpe {fmt_num(ref_out['sharpe'])}, Sortino {fmt_num(ref_out['sortino'])}, "
        f"CAGR {fmt_pct(ref_out['cagr'])}. Buy and hold: return {fmt_pct(ref_out['bh_return'])}, "
        f"Sharpe {fmt_num(ref_out['bh_sharpe'])}, Sortino {fmt_num(ref_out['bh_sortino'])}."
    )
    lines.append(
        f"Best of the 72 by out-of-sample Sharpe: {best[0].label()}. "
        f"Return {fmt_pct(best_out['return'])}, Sharpe {fmt_num(best_out['sharpe'])}, "
        f"Sortino {fmt_num(best_out['sortino'])}, CAGR {fmt_pct(best_out['cagr'])}."
    )
    if is_only:
        lines.append("In-sample only: " + "; ".join(item[0].label() for item in is_only) + ".")
    else:
        lines.append("No grid variant beat buy-and-hold Sharpe in-sample and failed out of sample.")
    lines.append("")
    lines.extend(diagnose_published_baseline())
    lines.append(
        f"With one position per pair, the same published signals run as baseline "
        f"close {baseline_pool['closed']} trades in 2017-2022 across the 20 series, "
        f"win rate {fmt_pct(baseline_pool['win_rate'])}, "
        f"average R {fmt_num(baseline_pool['expectancy'])}."
    )
    lines.append("")
    lines.append("## Published opposite, per pair")
    lines.append("")
    lines.append(
        "Stop is the round-2 rule: 0.25 ATR beyond the nearer of the mode level and the "
        "signal-bar wick. SMA filter on, long and short, at least one of 1w/3d/1d. "
        "Closed trades over the whole loaded history. Expectancy is mean R."
    )
    lines.append("")
    lines.append(
        "| Pair | Closed | Win rate | Avg win R | Avg loss R | Expectancy | Exits | Avg days |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    lines.extend(pair_lines)
    lines.append("")
    lines.append(
        f"Pooled out of sample: closed {reference_pool['closed']}, "
        f"win rate {fmt_pct(reference_pool['win_rate'])}, "
        f"average win R {fmt_num(reference_pool['avg_win_r'])}, "
        f"average loss R {fmt_num(reference_pool['avg_loss_r'])}, "
        f"expectancy {fmt_num(reference_pool['expectancy'])}, "
        f"average days {fmt_num(reference_pool['avg_days'])}. "
        f"Exits: {_reason_text(reference_pool['reasons'])}."
    )
    lines.append("")
    lines.append("## Anchor coverage")
    lines.append("")
    lines.append(
        "Share of the published signal set (SMA on, both directions, one decision timeframe) "
        "with a recorded anchor. A wrong-side anchor is still dropped when the stop is placed."
    )
    lines.append("")
    lines.append("| Anchor | Present | Signals |")
    lines.append("| --- | --- | --- |")
    for anchor, (present, total) in coverage.items():
        share = (present / total) if total else None
        lines.append(f"| {anchor} | {fmt_pct(share)} | {total} |")
    lines.append("")
    lines.append("## Ranked by out-of-sample Sharpe")
    lines.append("")
    lines.append(
        "| Rank | Variant | OOS closed | OOS win | OOS avg R | OOS return | OOS Sharpe | "
        "OOS Sortino | IS Sharpe | IS return | Flag |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    lines.append(
        f"|  | published stop | {reference_pool['closed']} | "
        f"{fmt_pct(reference_pool['win_rate'])} | "
        f"{fmt_num(reference_pool['expectancy'])} | {fmt_pct(ref_out['return'])} | "
        f"{fmt_num(ref_out['sharpe'])} | {fmt_num(ref_out['sortino'])} | "
        f"{fmt_num(reference['in']['sharpe'])} | {fmt_pct(reference['in']['return'])} | "
        f"{flag_of(reference)} |"
    )
    for rank, (spec, sample, pooled, _missed) in enumerate(rows, start=1):
        out = sample["out"]
        ins = sample["in"]
        lines.append(
            f"| {rank} | {spec.label()} | {pooled['closed']} | {fmt_pct(pooled['win_rate'])} | "
            f"{fmt_num(pooled['expectancy'])} | {fmt_pct(out['return'])} | "
            f"{fmt_num(out['sharpe'])} | "
            f"{fmt_num(out['sortino'])} | {fmt_num(ins['sharpe'])} | {fmt_pct(ins['return'])} | "
            f"{flag_of(sample)} |"
        )
    lines.append("")
    lines.append("## Equity curve")
    lines.append("")
    lines.append("![Equal-weight portfolio](portfolio_equity.png)")
    lines.append("")
    lines.append(
        "Log scale, growth of 1. The dashed line is 2023-01-01. "
        "Buy and hold is the same equal-weight daily-return book."
    )
    lines.append("")
    start, end = "2017-01-01", "2026-12-31"
    curves = [
        ("Buy and hold", buy_hold_curve(published, start, end)),
        ("Published opposite", compound(published, start, end)),
        (f"Best OOS: {best[0].label()}", compound(best_sleeves, start, end)),
    ]
    draw(curves, REPORTS / "portfolio_equity.png")
    return "\n".join(lines) + "\n"


def beats_sample(stats: dict) -> bool:
    return (
        stats["sharpe"] is not None
        and stats["bh_sharpe"] is not None
        and stats["sharpe"] > stats["bh_sharpe"]
    )


def flag_of(sample: dict) -> str:
    if (
        sample["in"]["sharpe"] is not None
        and sample["in"]["bh_sharpe"] is not None
        and sample["in"]["sharpe"] > sample["in"]["bh_sharpe"]
        and not beats_sample(sample["out"])
    ):
        return "IS only"
    if beats_sample(sample["out"]):
        return "beats OOS"
    return ""


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
