"""ExchangeAccount controller."""

from Core.http import list_response
from Repositories.ExchangeAccounts.middlewares.exchange_account_middleware import (
    ExchangeAccountListQuery,
)
from Repositories.ExchangeAccounts.modules import exchange_account_module


async def get(params: ExchangeAccountListQuery) -> dict:
    data = await exchange_account_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
