"""Symbol routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Symbols.controllers import symbol_controller
from Repositories.Symbols.middlewares.symbol_middleware import SymbolListQuery

router = APIRouter(
    prefix="/symbols",
    tags=["symbols"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List monitored pairs. Planning skeleton: empty page.")
async def list_symbols(params: SymbolListQuery = Depends()) -> dict:
    return await symbol_controller.get(params)
