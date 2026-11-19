"""Grok Bot feed. The skeleton has no rows to return."""

from typing import Any


async def feed(params: dict, auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    limit = min(max(int(params.get("limit") or 50), 1), 100)
    return {"data": [], "cursor": None, "limit": limit}
