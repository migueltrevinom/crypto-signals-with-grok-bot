"""Candle controller. Calls the module and shapes the list envelope."""

from Core.http import list_response
from Repositories.MarketData.middlewares.candle_middleware import CandleListQuery
from Repositories.MarketData.modules import candle_module


async def get(params: CandleListQuery) -> dict:
    data = await candle_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
