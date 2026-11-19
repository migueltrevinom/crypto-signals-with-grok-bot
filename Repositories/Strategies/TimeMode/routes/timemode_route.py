"""Time@mode routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Strategies.TimeMode.controllers import timemode_controller

router = APIRouter(
    prefix="/strategies/time-mode",
    tags=["strategies"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="Active time@mode defaults from prototype/config.json. Not persisted.")
async def show_time_mode() -> dict:
    return await timemode_controller.show_active()
