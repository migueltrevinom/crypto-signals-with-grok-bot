"""Exchange routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Exchanges.controllers import exchange_controller

router = APIRouter(
    prefix="/exchanges",
    tags=["exchanges"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="CEX catalog with native intervals and symbol style. Not stored.")
async def list_exchanges() -> dict:
    return await exchange_controller.list_sources()
