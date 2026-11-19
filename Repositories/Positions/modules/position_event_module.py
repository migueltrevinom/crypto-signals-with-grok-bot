"""PositionEvent reads.

Planning skeleton: empty page, no Mongo read. Phase work replaces this
body with Core.mongo_orm.build_query.
"""

from Core.http import empty_page, page_args


async def get(params: dict, auth_user: dict | None = None) -> dict:
    del auth_user
    page, limit = page_args(params)
    return empty_page(page, limit)
