"""Pull feed. Ack is specified and not mounted in this pass."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Alerts.controllers import alert_feed_controller
from Repositories.Alerts.middlewares.alert_feed_middleware import AlertFeedQuery

router = APIRouter(
    prefix="/alerts/feed",
    tags=["alerts"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="Alerts waiting for the Grok Bot. Empty in this pass.")
async def alert_feed(params: AlertFeedQuery = Depends()) -> dict:
    return await alert_feed_controller.feed(params.model_dump())
