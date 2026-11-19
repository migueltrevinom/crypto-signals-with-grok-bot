"""Worker scheduler seam.

Phase 1 fills this with APScheduler inside the worker process, at
SCAN_INTERVAL_SECONDS. The API process does not run the schedule.
Not a dependency in the planning skeleton.
"""

from collections.abc import Awaitable, Callable


def schedule_interval(seconds: int, job: Callable[[], Awaitable[None]]) -> None:
    del seconds, job
    raise NotImplementedError(
        "The worker schedule is added with the scanner port. See docs/architecture.md."
    )
