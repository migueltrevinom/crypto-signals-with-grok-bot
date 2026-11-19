"""Scanner process. Public klines only. No orders and no exchange API keys.

`--once` runs one pass (the same job as `python -m scripts.scan_once`).
`--schedule` wakes at minute 2 of every hour, shortly after candle closes.
"""

import argparse
import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scripts.scan_once import scan

from Core.config import get_settings
from Core.logging import configure_logging

logger = logging.getLogger("app.worker")


def run_once() -> int:
    asyncio.run(scan(echo=True))
    return 0


async def _scheduled() -> None:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(scan, "cron", minute=2)
    scheduler.start()
    logger.info("scheduler armed for minute 2 of every hour")
    await asyncio.Event().wait()


def main(argv: list[str] | None = None) -> int:
    settings = get_settings()
    configure_logging(settings.log_level)
    parser = argparse.ArgumentParser(description="time@mode scanner worker")
    parser.add_argument("--once", action="store_true", help="scan once and print new signals")
    parser.add_argument("--schedule", action="store_true", help="scan shortly after each hour")
    args = parser.parse_args(argv)
    if args.schedule:
        asyncio.run(_scheduled())
        return 0
    if args.once:
        return run_once()
    logger.info(
        "idle. Use --once or --schedule (interval setting %ss).",
        settings.scan_interval_seconds,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
