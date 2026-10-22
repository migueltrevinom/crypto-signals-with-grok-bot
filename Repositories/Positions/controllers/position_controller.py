"""Position controller."""

from Core.http import list_response
from Repositories.Positions.middlewares.position_middleware import PositionListQuery
from Repositories.Positions.modules import position_module


async def get(params: PositionListQuery) -> dict:
    data = await position_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
