"""Full historical matrix. No parameter search. No live orders.

Writes reports/summary.md and reports/trades-{exchange}-{symbol}.csv.
Candle pages are cached under reports/.cache so a rerun does not refetch.
"""

import argparse
import asyncio
import csv
import sys
import traceback
from datetime import UTC, datetime

from Core.config import REPO_ROOT
from Repositories.MarketData.modules.candles import LADDER
from Repositories.PaperTrading.modules.simulator import DEFAULT_EQUITY, EXIT_MODES, simulate
from Repositories.Signals.modules.engine_module import prepare
from scripts.history import get_series
from scripts.stats import (
    IN_SAMPLE,
    OUT_OF_SAMPLE,
    REGIMES,
    fmt_num,
    fmt_pct,
    portfolio_metrics,
    window_metrics,
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


def _row(label: str, stats: dict) -> str:
    return (
        f"| {label} | {stats['closed']} | {fmt_pct(stats['win_rate'])} | "
        f"{fmt_num(stats['avg_r'])} | {fmt_pct(stats['realized'] / DEFAULT_EQUITY)} | "
        f"{fmt_pct(stats['unrealized'] / DEFAULT_EQUITY)} | {fmt_num(stats['sharpe'])} | "
        f"{fmt_num(stats['sortino'])} | {fmt_pct(stats['cagr'])} | {fmt_pct(stats['exposure'])} | "
        f"{fmt_num(stats['avg_days'])} | {fmt_pct(stats['max_dd'])} | {fmt_pct(stats['return'])} | "
        f"{fmt_pct(stats['buy_hold'])} | {fmt_num(stats['buy_hold_sharpe'])} |"
    )


HEADER = (
    "| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | "
    "CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |"
)
RULE = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"


async def run_one(exchange: str, symbol: str) -> dict:
    print(f"[fetch] {exchange} {symbol}", file=sys.stderr)
    series = await get_series(exchange, symbol, HISTORY_START)
    counts = {tf: len(series.get(tf, [])) for tf in LADDER}
    print(f"[bars] {exchange} {symbol} {counts}", file=sys.stderr)
    if len(series.get("1d", [])) < 80 or len(series.get("6h", [])) < 80:
        return {"exchange": exchange, "symbol": symbol, "error": "not enough history", "trades": []}
    entries, trails = prepare(exchange, symbol, series)
    variants = {}
    rows = []
    for name in EXIT_MODES:
        result = simulate(entries, series, equity=DEFAULT_EQUITY, exit_mode=name, trails=trails)
        variants[name] = result
        rows.extend(result.trades)
        print(
            f"[done] {exchange} {symbol} {name} signals={len(entries)} "
            f"trades={len(result.trades)} blocked={result.blocked} cash={result.equity:.0f}",
            file=sys.stderr,
        )
    path = REPORTS / f"trades-{exchange}-{symbol}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "variant",
                "signal_id",
                "exchange",
                "symbol",
                "timeframe",
                "direction",
                "opened_at",
                "closed_at",
                "entry",
                "stop",
                "exit",
                "exit_reason",
                "realized",
                "size",
                "pnl",
                "r_multiple",
                "fee",
            ],
        )
        writer.writeheader()
        for trade in rows:
            writer.writerow(
                {
                    "variant": trade.variant,
                    "signal_id": trade.signal_id,
                    "exchange": trade.exchange,
                    "symbol": trade.symbol,
                    "timeframe": trade.timeframe,
                    "direction": trade.direction,
                    "opened_at": trade.opened_at.isoformat(),
                    "closed_at": trade.closed_at.isoformat() if trade.closed_at else "",
                    "entry": trade.entry,
                    "stop": trade.stop,
                    "exit": trade.exit,
                    "exit_reason": trade.exit_reason,
                    "realized": trade.realized,
                    "size": trade.size,
                    "pnl": trade.pnl,
                    "r_multiple": trade.r_multiple,
                    "fee": trade.fee,
                }
            )
    return {
        "exchange": exchange,
        "symbol": symbol,
        "error": None,
        "variants": variants,
        "daily": series.get("1d", []),
        "signals": len(entries),
        "first": series["1d"][0].open_time.date().isoformat() if series.get("1d") else None,
        "last": series["1d"][-1].close_time.date().isoformat() if series.get("1d") else None,
    }


def _metrics(result: dict, variant: str, start: str, end: str) -> dict:
    sim = result["variants"][variant]
    return window_metrics(sim.trades, result["daily"], start, end, blocked=sim.blocked)


def render(results: list[dict]) -> str:
    lines = [
        "# time@mode paper backtest",
        "",
        "Baseline exit rules: fixed stop, or two closes back inside the level.",
        "No parameter optimization. Fees are 0.1% taker per side. Slippage is 5 bps.",
        "Starting equity is 10,000 USDT per pair. One position per direction.",
        "Win rate and average R use closed trades only. Realized is closed PnL in the window",
        "as a percent of starting equity. Unrealized is the open mark at the window end.",
        "Return, Sharpe, Sortino, and CAGR mark the book to the daily close, including",
        "positions opened before the window. Buy-and-hold is the daily close change.",
        "In-sample is 2017-2022 and out-of-sample is 2023 onward.",
        "Ten USDT symbols on Binance and KuCoin, twenty series.",
        "The other exit rules are in reports/exit_variants.md.",
        "",
    ]
    for result in results:
        lines.append(f"## {result['exchange']} {result['symbol']}")
        lines.append("")
        if result.get("error"):
            lines.append(f"Skipped: {result['error']}.")
            lines.append("")
            continue
        sim = result["variants"]["baseline"]
        lines.append(
            f"History {result['first']} to {result['last']}. Signals {result['signals']}. "
            f"Blocked {sim.blocked}."
        )
        lines.append("")
        lines.append(HEADER)
        lines.append(RULE)
        for name, start, end in (IN_SAMPLE, OUT_OF_SAMPLE, *REGIMES):
            lines.append(_row(name, _metrics(result, "baseline", start, end)))
        lines.append("")
    return "\n".join(lines) + "\n"


def _portfolio(results: list[dict], variant: str, start: str, end: str) -> dict:
    sleeves = []
    for result in results:
        if result.get("error"):
            continue
        sleeves.append((result["variants"][variant].trades, result["daily"]))
    if not sleeves:
        return {
            "sharpe": None,
            "sortino": None,
            "cagr": None,
            "return": None,
            "bh_sharpe": None,
            "bh_return": None,
            "pairs": 0,
        }
    return portfolio_metrics(sleeves, start, end)


def render_variants(results: list[dict]) -> str:
    lines = [
        "# Exit variants",
        "",
        "Same signals and the same 0.7 ATR readings. Only the exit setting changes.",
        "baseline: fixed stop or two closes. trail: stop ratchets to the confirmed",
        "5-bar swing or the new block on the timeframe in control. opposite: an",
        "opposite confirmed signal closes the trade and may reverse. two_close:",
        "the two-close rule only. all: stop, trail, opposite, and two closes together.",
        "The portfolio is the equal-weight of each pair's daily return, both exchanges together.",
        "A variant that beats that portfolio's buy-and-hold Sharpe in 2017-2022 and does not",
        "beat it in 2023-now is marked in-sample only.",
        "",
    ]
    lines.append(
        "| Variant | Sample | Pairs | Return | Sharpe | Sortino | CAGR | "
        "BH return | BH Sharpe | BH Sortino | Beats BH Sharpe |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    flags = []
    for variant in EXIT_MODES:
        sample = {}
        for label, start, end in (IN_SAMPLE, OUT_OF_SAMPLE):
            stats = _portfolio(results, variant, start, end)
            sample[label] = stats
            beats = (
                stats["sharpe"] is not None
                and stats["bh_sharpe"] is not None
                and stats["sharpe"] > stats["bh_sharpe"]
            )
            lines.append(
                f"| {variant} | {label} | {stats['pairs']} | {fmt_pct(stats['return'])} | "
                f"{fmt_num(stats['sharpe'])} | {fmt_num(stats['sortino'])} | "
                f"{fmt_pct(stats['cagr'])} | "
                f"{fmt_pct(stats['bh_return'])} | {fmt_num(stats['bh_sharpe'])} | "
                f"{fmt_num(stats['bh_sortino'])} | {'yes' if beats else 'no'} |"
            )
        ins = sample[IN_SAMPLE[0]]
        outs = sample[OUT_OF_SAMPLE[0]]
        in_beats = (
            ins["sharpe"] is not None
            and ins["bh_sharpe"] is not None
            and ins["sharpe"] > ins["bh_sharpe"]
        )
        out_beats = (
            outs["sharpe"] is not None
            and outs["bh_sharpe"] is not None
            and outs["sharpe"] > outs["bh_sharpe"]
        )
        if in_beats and not out_beats:
            flags.append(variant)
        in_sortino = (
            ins["sortino"] is not None
            and ins["bh_sortino"] is not None
            and ins["sortino"] > ins["bh_sortino"]
        )
        out_sortino = (
            outs["sortino"] is not None
            and outs["bh_sortino"] is not None
            and outs["sortino"] > outs["bh_sortino"]
        )
        if in_sortino and not out_sortino and variant not in flags:
            flags.append(f"{variant} (Sortino only)")
    lines.append("")
    if flags:
        lines.append("In-sample only: " + ", ".join(flags) + ".")
    else:
        lines.append("No variant beat buy-and-hold Sharpe in-sample and failed out of sample.")
    lines.append("")
    oos = {
        name: _portfolio(results, name, OUT_OF_SAMPLE[1], OUT_OF_SAMPLE[2])
        for name in EXIT_MODES
    }
    winners = [
        name
        for name, stats in oos.items()
        if stats["sharpe"] is not None
        and stats["bh_sharpe"] is not None
        and stats["sharpe"] > stats["bh_sharpe"]
    ]
    if winners:
        lines.append(
            "Out of sample, these variants beat equal-weight buy-and-hold Sharpe: "
            + ", ".join(winners)
            + "."
        )
    else:
        lines.append(
            "Out of sample, no variant beat equal-weight buy-and-hold Sharpe."
        )
    lines.append("")
    for result in results:
        if result.get("error"):
            continue
        lines.append(f"## {result['exchange']} {result['symbol']}")
        lines.append("")
        for variant, sim in result["variants"].items():
            reasons: dict[str, int] = {}
            for trade in sim.trades:
                reasons[trade.exit_reason] = reasons.get(trade.exit_reason, 0) + 1
            reason_text = ", ".join(f"{key} {value}" for key, value in sorted(reasons.items()))
            lines.append(f"### {variant}")
            lines.append("")
            lines.append(f"Blocked signals {sim.blocked}. Exits: {reason_text}.")
            lines.append("")
            lines.append(HEADER)
            lines.append(RULE)
            for name, start, end in (IN_SAMPLE, OUT_OF_SAMPLE):
                lines.append(_row(name, _metrics(result, variant, start, end)))
            lines.append("")
    return "\n".join(lines) + "\n"


async def main_async(exchanges: list[str], symbols: list[str]) -> None:
    results = []
    for exchange in exchanges:
        for symbol in symbols:
            try:
                results.append(await run_one(exchange, symbol))
            except Exception as exc:
                print(f"[error] {exchange} {symbol} {exc}", file=sys.stderr)
                traceback.print_exc()
                results.append(
                    {"exchange": exchange, "symbol": symbol, "error": str(exc), "trades": []}
                )
    REPORTS.mkdir(parents=True, exist_ok=True)
    text = render(results)
    (REPORTS / "summary.md").write_text(text, encoding="utf-8")
    variants = render_variants(results)
    (REPORTS / "exit_variants.md").write_text(variants, encoding="utf-8")
    print(variants)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the time@mode paper backtest matrix")
    parser.add_argument("--exchange", action="append", choices=EXCHANGES)
    parser.add_argument("--symbols", default=",".join(SYMBOLS))
    args = parser.parse_args()
    exchanges = args.exchange or list(EXCHANGES)
    symbols = [item.strip() for item in args.symbols.split(",") if item.strip()]
    asyncio.run(main_async(exchanges, symbols))


if __name__ == "__main__":
    main()
