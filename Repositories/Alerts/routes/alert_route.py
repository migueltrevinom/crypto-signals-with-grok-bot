"""Alert routes. Thin: auth dependency, validation, controller."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Alerts.controllers import alert_controller
from Repositories.Alerts.middlewares.alert_middleware import AlertListQuery

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List alert deliveries. Planning skeleton: empty page, no Mongo read.")
async def list_alerts(params: AlertListQuery = Depends()) -> dict:
    return await alert_controller.get(params)
