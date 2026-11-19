"""PositionEvent routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Positions.controllers import position_event_controller
from Repositories.Positions.middlewares.position_event_middleware import PositionEventListQuery

router = APIRouter(
    prefix="/position-events",
    tags=["positions"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List position events. Planning skeleton: empty page.")
async def list_position_events(params: PositionEventListQuery = Depends()) -> dict:
    return await position_event_controller.get(params)
