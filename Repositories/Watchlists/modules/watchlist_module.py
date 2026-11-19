"""Watchlist reads and writes.

Planning skeleton: returns an empty page and does not call build_query.
Phase 2 replaces the body with Core.mongo_orm.build_query. Do not query
Motor or Beanie find() from this module.
"""

from Core.http import empty_page, page_args


async def get(params: dict, auth_user: dict | None = None) -> dict:
    del auth_user
    page, limit = page_args(params)
    return empty_page(page, limit)
