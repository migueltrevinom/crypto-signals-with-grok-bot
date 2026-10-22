"""Settings controller."""

from Repositories.Settings.modules import settings_module


async def show_ladder() -> dict:
    return {"data": await settings_module.show_ladder(auth_user=None)}


async def show_scanner() -> dict:
    return {"data": await settings_module.show_scanner(auth_user=None)}


async def show_arbitrage() -> dict:
    return {"data": await settings_module.show_arbitrage(auth_user=None)}
