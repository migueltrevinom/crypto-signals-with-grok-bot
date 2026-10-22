"""DEX routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Dexes.controllers import dex_controller

router = APIRouter(
    prefix="/dexes",
    tags=["dexes"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="DEX connector seed. Disabled. No quotes and no swaps.")
async def list_dexes() -> dict:
    return await dex_controller.list_venues()
