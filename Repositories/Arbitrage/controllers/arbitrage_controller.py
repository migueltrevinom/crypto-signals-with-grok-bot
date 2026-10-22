"""Arbitrage controller."""

from Core.http import list_response
from Repositories.Arbitrage.middlewares.arbitrage_middleware import ArbitrageListQuery
from Repositories.Arbitrage.modules import arbitrage_module


async def get(params: ArbitrageListQuery) -> dict:
    data = await arbitrage_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
