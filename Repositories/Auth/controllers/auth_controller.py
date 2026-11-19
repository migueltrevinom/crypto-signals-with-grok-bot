"""Auth controller."""

from Repositories.Auth.modules import auth_module


async def show_config() -> dict:
    return {"data": await auth_module.show_config(auth_user=None)}
