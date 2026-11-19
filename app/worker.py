"""Scanner process.

The planning skeleton does not fetch candles or run detection. `--once`
logs that and exits 0, which is the command the docs and tests use.
The real loop arrives with the port (docs/roadmap.md, phase 1).
"""

import argparse
import logging

from Core.config import get_settings
from Core.logging import configure_logging

logger = logging.getLogger("app.worker")


def main(argv: list[str] | None = None) -> int:
    settings = get_settings()
    configure_logging(settings.log_level)
    parser = argparse.ArgumentParser(description="time@mode scanner worker")
    parser.add_argument(
        "--once",
        action="store_true",
        help="single pass. The skeleton always exits; this flag is the supported entry.",
    )
    args = parser.parse_args(argv)
    logger.info(
        "worker skeleton: detection is not ported (interval=%ss, once=%s)",
        settings.scan_interval_seconds,
        args.once,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
