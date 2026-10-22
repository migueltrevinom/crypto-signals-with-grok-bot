"""Signal routes. Thin: auth dependency, validation, controller."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Signals.controllers import signal_controller
from Repositories.Signals.middlewares.signal_middleware import SignalListQuery

router = APIRouter(
    prefix="/signals",
    tags=["signals"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List stored signals. Planning skeleton: empty page, no Mongo read.")
async def list_signals(params: SignalListQuery = Depends()) -> dict:
    return await signal_controller.get(params)
