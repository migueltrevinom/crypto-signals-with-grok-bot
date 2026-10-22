"""Candle routes. Thin: auth dependency, validation, controller."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.MarketData.controllers import candle_controller
from Repositories.MarketData.middlewares.candle_middleware import CandleListQuery

router = APIRouter(
    prefix="/market-data",
    tags=["market-data"],
    dependencies=[Depends(require_api_key)],
)


@router.get(
    "/candles",
    summary="List cached candles. Planning skeleton: empty page, no fetch.",
)
async def list_candles(params: CandleListQuery = Depends()) -> dict:
    return await candle_controller.get(params)
