"""Subscription controller."""

from Core.http import list_response
from Repositories.Billing.middlewares.subscription_middleware import SubscriptionListQuery
from Repositories.Billing.modules import subscription_module


async def get(params: SubscriptionListQuery) -> dict:
    data = await subscription_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
