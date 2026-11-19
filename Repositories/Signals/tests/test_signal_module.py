"""Signals module stub. Persistence is asserted once build_query exists."""

import asyncio

from Repositories.Signals.modules import signal_module


def test_get_returns_an_empty_page() -> None:
    result = asyncio.run(signal_module.get({"page": 2, "limit": 5}))
    assert result == {"docs": [], "total": 0, "limit": 5, "page": 2, "pages": 0}
