"""Worker flags. The once-path is patched so tests do not hit exchanges."""

from app import worker


def test_worker_once_exits_cleanly(monkeypatch) -> None:
    monkeypatch.setattr(worker, "run_once", lambda: 0)
    assert worker.main(["--once"]) == 0


def test_worker_without_flags_also_exits() -> None:
    assert worker.main([]) == 0
