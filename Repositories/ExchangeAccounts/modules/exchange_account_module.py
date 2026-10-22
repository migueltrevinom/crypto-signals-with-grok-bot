"""ExchangeAccount list. Planning skeleton: empty page, no Mongo read."""

from Core.http import empty_page, page_args


async def get(params: dict, auth_user: dict | None = None) -> dict:
    del auth_user
    page, limit = page_args(params)
    return empty_page(page, limit)
