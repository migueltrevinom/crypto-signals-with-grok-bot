"""Confluence controller."""

from Core.http import list_response
from Repositories.Strategies.Confluence.modules import confluence_module


async def show_config() -> dict:
    return {"data": await confluence_module.show_config(auth_user=None)}


async def list_entry_plans(params: dict) -> dict:
    return list_response(await confluence_module.list_entry_plans(params, auth_user=None))
