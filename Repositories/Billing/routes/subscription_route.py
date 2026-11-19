"""Subscription routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Billing.controllers import subscription_controller
from Repositories.Billing.middlewares.subscription_middleware import SubscriptionListQuery

router = APIRouter(
    prefix="/subscriptions",
    tags=["billing"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List subscriptions. Empty. No charges.")
async def list_subscriptions(params: SubscriptionListQuery = Depends()) -> dict:
    return await subscription_controller.get(params)
