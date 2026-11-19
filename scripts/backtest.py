"""Single-slice wrapper around the matrix.

Example:
  python -m scripts.backtest --exchange binance --symbols BTCUSDT,ETHUSDT --start 2023-01-01
"""

import argparse
import asyncio
import sys

from scripts.backtest_matrix import EXCHANGES, main_async


def main() -> None:
    parser = argparse.ArgumentParser(description="Paper backtest. No live orders.")
    parser.add_argument("--exchange", required=True, choices=EXCHANGES)
    parser.add_argument("--symbols", required=True)
    parser.add_argument("--start", default="2017-01-01")
    args = parser.parse_args()
    if args.start != "2017-01-01":
        print(
            "This run still loads cached history from 2017 and reports every regime. "
            f"Requested start {args.start} is noted; the matrix is not refit.",
            file=sys.stderr,
        )
    symbols = [item.strip() for item in args.symbols.split(",") if item.strip()]
    asyncio.run(main_async([args.exchange], symbols))


if __name__ == "__main__":
    main()
