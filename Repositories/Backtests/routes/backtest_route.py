"""Backtest routes. Thin: auth dependency, validation, controller."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Backtests.controllers import backtest_controller
from Repositories.Backtests.middlewares.backtest_middleware import BacktestListQuery

router = APIRouter(
    prefix="/backtests",
    tags=["backtests"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List backtests. Planning skeleton: empty page, no Mongo read.")
async def list_backtests(params: BacktestListQuery = Depends()) -> dict:
    return await backtest_controller.get(params)
