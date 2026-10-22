"""Backtest controller. Calls the module and shapes the list envelope."""

from Core.http import list_response
from Repositories.Backtests.middlewares.backtest_middleware import BacktestListQuery
from Repositories.Backtests.modules import backtest_module


async def get(params: BacktestListQuery) -> dict:
    data = await backtest_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
