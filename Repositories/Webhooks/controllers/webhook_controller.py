"""Webhook controller."""

from Core.http import list_response
from Repositories.Webhooks.middlewares.webhook_middleware import WebhookListQuery
from Repositories.Webhooks.modules import webhook_endpoint_module


async def list_endpoints(params: WebhookListQuery) -> dict:
    data = await webhook_endpoint_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
