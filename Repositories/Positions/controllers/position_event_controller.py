"""PositionEvent controller."""

from Core.http import list_response
from Repositories.Positions.middlewares.position_event_middleware import PositionEventListQuery
from Repositories.Positions.modules import position_event_module


async def get(params: PositionEventListQuery) -> dict:
    data = await position_event_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
