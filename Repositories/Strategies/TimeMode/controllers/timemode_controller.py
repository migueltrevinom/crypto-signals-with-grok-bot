"""Time@mode controller."""

from Repositories.Strategies.TimeMode.modules import timemode_module


async def show_active() -> dict:
    return {"data": await timemode_module.show_active(auth_user=None)}
