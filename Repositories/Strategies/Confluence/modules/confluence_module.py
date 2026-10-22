"""Confluence config seed. Scoring is specified and not implemented."""

from typing import Any

from Core.http import empty_page, page_args
from Core.planning_seeds import CONFLUENCE_SEED


async def show_config(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    return dict(CONFLUENCE_SEED)


async def list_entry_plans(params: dict, auth_user: dict | None = None) -> dict:
    del auth_user
    page, limit = page_args(params)
    return empty_page(page, limit)
