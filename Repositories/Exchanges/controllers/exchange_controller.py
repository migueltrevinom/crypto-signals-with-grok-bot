"""Exchange controller. The list is not a paged collection in the skeleton."""

from Repositories.Exchanges.modules import exchange_module


async def list_sources() -> dict:
    return {"data": await exchange_module.list_sources(auth_user=None)}
