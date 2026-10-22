"""DEX controller."""

from Repositories.Dexes.modules import dex_module


async def list_venues() -> dict:
    return {"data": await dex_module.list_venues(auth_user=None)}
