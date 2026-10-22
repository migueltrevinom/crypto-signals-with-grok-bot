"""AlertChannel routes. Thin: auth dependency, validation, controller."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Alerts.controllers import alert_channel_controller
from Repositories.Alerts.middlewares.alert_channel_middleware import AlertChannelListQuery

router = APIRouter(
    prefix="/alert-channels",
    tags=["alert-channels"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List alert channels. Planning skeleton: empty page, no Mongo read.")
async def list_alert_channels(params: AlertChannelListQuery = Depends()) -> dict:
    return await alert_channel_controller.get(params)
