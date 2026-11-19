"""DEX catalog seed. Quotes are not fetched."""

from typing import Any

from Core.planning_seeds import DEX_CATALOG


async def list_venues(auth_user: dict | None = None) -> list[dict[str, Any]]:
    del auth_user
    return [{**row, "persisted": False} for row in DEX_CATALOG]
