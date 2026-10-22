"""Webhook endpoint list. Signing is specified and not implemented."""

from Core.http import empty_page, page_args


async def get(params: dict, auth_user: dict | None = None) -> dict:
    del auth_user
    page, limit = page_args(params)
    return empty_page(page, limit)
