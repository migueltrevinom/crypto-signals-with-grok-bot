"""ExchangeAccount routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.ExchangeAccounts.controllers import exchange_account_controller
from Repositories.ExchangeAccounts.middlewares.exchange_account_middleware import (
    ExchangeAccountListQuery,
)

router = APIRouter(
    prefix="/exchange-accounts",
    tags=["exchange-accounts"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List exchange accounts. Empty. Keys are not accepted.")
async def list_exchange_accounts(params: ExchangeAccountListQuery = Depends()) -> dict:
    return await exchange_account_controller.get(params)
