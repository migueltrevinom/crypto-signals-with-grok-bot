"""List webhook endpoints. POST is not mounted. Secrets are never listed."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Webhooks.controllers import webhook_controller
from Repositories.Webhooks.middlewares.webhook_middleware import WebhookListQuery

router = APIRouter(
    prefix="/webhooks/endpoints",
    tags=["webhooks"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="Signed outbound webhook endpoints. Empty. No exchange keys.")
async def list_webhook_endpoints(params: WebhookListQuery = Depends()) -> dict:
    return await webhook_controller.list_endpoints(params)
