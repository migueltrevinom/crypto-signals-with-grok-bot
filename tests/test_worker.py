"""The skeleton worker exits without scanning."""

from app.worker import main


def test_worker_once_exits_cleanly() -> None:
    assert main(["--once"]) == 0


def test_worker_without_flags_also_exits() -> None:
    assert main([]) == 0
