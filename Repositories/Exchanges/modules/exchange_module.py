"""CEX catalog from the planning seed. Not fetched and not stored."""

from typing import Any

from Core.planning_seeds import EXCHANGE_CATALOG


async def list_sources(auth_user: dict | None = None) -> list[dict[str, Any]]:
    del auth_user
    return [{**row, "persisted": False} for row in EXCHANGE_CATALOG]
