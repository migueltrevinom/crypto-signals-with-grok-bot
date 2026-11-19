"""Settings routes. Seeds only. PUT is specified and not mounted."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Settings.controllers import settings_controller

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/ladder", summary="Ladder seed, including the 6h SMA filter. Not stored.")
async def show_ladder() -> dict:
    return await settings_controller.show_ladder()


@router.get("/scanner", summary="Scanner seed. The old ltf_map is not part of it.")
async def show_scanner() -> dict:
    return await settings_controller.show_scanner()


@router.get("/arbitrage", summary="Arbitrage cost seed. Orders stay off.")
async def show_arbitrage() -> dict:
    return await settings_controller.show_arbitrage()
