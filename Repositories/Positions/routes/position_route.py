"""Position routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Positions.controllers import position_controller
from Repositories.Positions.middlewares.position_middleware import PositionListQuery

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List planned positions. Planning skeleton: empty page.")
async def list_positions(params: PositionListQuery = Depends()) -> dict:
    return await position_controller.get(params)
