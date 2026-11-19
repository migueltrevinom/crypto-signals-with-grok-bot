"""Arbitrage routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Arbitrage.controllers import arbitrage_controller
from Repositories.Arbitrage.middlewares.arbitrage_middleware import ArbitrageListQuery

router = APIRouter(
    prefix="/arbitrage",
    tags=["arbitrage"],
    dependencies=[Depends(require_api_key)],
)


@router.get(
    "/opportunities",
    summary="List arbitrage opportunities. Empty page. No orders.",
)
async def list_opportunities(params: ArbitrageListQuery = Depends()) -> dict:
    return await arbitrage_controller.get(params)
