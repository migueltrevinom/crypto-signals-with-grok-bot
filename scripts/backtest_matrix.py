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
from Repositories.PaperTrading.modules.simulator import DEFAULT_EQUITY, simulate
from Repositories.Signals.modules.engine_module import build_entries
from scripts.history import get_series
from scripts.stats import (
    IN_SAMPLE,
    OUT_OF_SAMPLE,
    REGIMES,
    buy_and_hold,
    fmt_num,
    fmt_pct,
    in_window,
    summarize,
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


def _cell(trades, daily, start: str, end: str) -> dict:
    selected = [trade for trade in trades if in_window(trade.opened_at, start, end)]
    stats = summarize(selected)
    stats["buy_hold"] = buy_and_hold(daily, start, end)
    return stats


def _row(label: str, stats: dict) -> str:
    return (
        f"| {label} | {stats['trades']} | {fmt_pct(stats['win_rate'])} | "
        f"{fmt_num(stats['avg_r'])} | {fmt_num(stats['expectancy'])} | "
        f"{fmt_num(stats['profit_factor'])} | {fmt_pct(stats['max_dd'])} | "
        f"{fmt_pct(stats['return'])} | {fmt_pct(stats['buy_hold'])} |"
    )


async def run_one(exchange: str, symbol: str) -> dict:
    print(f"[fetch] {exchange} {symbol}", file=sys.stderr)
    series = await get_series(exchange, symbol, HISTORY_START)
    counts = {tf: len(series.get(tf, [])) for tf in LADDER}
    print(f"[bars] {exchange} {symbol} {counts}", file=sys.stderr)
    if len(series.get("1d", [])) < 80 or len(series.get("6h", [])) < 80:
        return {"exchange": exchange, "symbol": symbol, "error": "not enough history", "trades": []}
    entries = build_entries(exchange, symbol, series)
    trades, equity = simulate(entries, series, equity=DEFAULT_EQUITY)
    print(
        f"[done] {exchange} {symbol} signals={len(entries)} "
        f"trades={len(trades)} equity={equity:.0f}",
        file=sys.stderr,
    )
    path = REPORTS / f"trades-{exchange}-{symbol}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
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
                "size",
                "pnl",
                "r_multiple",
                "fee",
            ],
        )
        writer.writeheader()
        for trade in trades:
            writer.writerow(
                {
                    "signal_id": trade.signal_id,
                    "exchange": trade.exchange,
                    "symbol": trade.symbol,
                    "timeframe": trade.timeframe,
                    "direction": trade.direction,
                    "opened_at": trade.opened_at.isoformat(),
                    "closed_at": trade.closed_at.isoformat(),
                    "entry": trade.entry,
                    "stop": trade.stop,
                    "exit": trade.exit,
                    "exit_reason": trade.exit_reason,
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
        "trades": trades,
        "daily": series.get("1d", []),
        "signals": len(entries),
        "first": series["1d"][0].open_time.date().isoformat() if series.get("1d") else None,
        "last": series["1d"][-1].close_time.date().isoformat() if series.get("1d") else None,
    }


def render(results: list[dict]) -> str:
    lines = [
        "# time@mode paper backtest",
        "",
        "No parameter optimization. Fees are 0.1% taker per side. Slippage is 5 bps.",
        "Starting equity is 10,000 USDT per pair. One position at a time.",
        "R is net PnL divided by the 1% risk budget. Buy-and-hold is the daily close change.",
        "In-sample is 2017-2022 and out-of-sample is 2023 onward. The same rules run on both.",
        "",
    ]
    header = (
        "| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | "
        "Strategy | Buy & hold |"
    )
    rule = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    for result in results:
        lines.append(f"## {result['exchange']} {result['symbol']}")
        lines.append("")
        if result.get("error"):
            lines.append(f"Skipped: {result['error']}.")
            lines.append("")
            continue
        lines.append(f"History {result['first']} to {result['last']}. Signals {result['signals']}.")
        lines.append("")
        lines.append(header)
        lines.append(rule)
        daily = result["daily"]
        trades = result["trades"]
        for name, start, end in (IN_SAMPLE, OUT_OF_SAMPLE, *REGIMES):
            lines.append(_row(name, _cell(trades, daily, start, end)))
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
    print(text)


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
