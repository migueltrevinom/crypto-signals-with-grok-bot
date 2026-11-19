"""Public plan list. Prices are null until competitive pricing is filled in."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Billing.controllers import billing_controller

router = APIRouter(
    prefix="/plans",
    tags=["billing"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="Seed tiers. price_cents is null. Not stored.")
async def list_plans() -> dict:
    return await billing_controller.list_plans()
