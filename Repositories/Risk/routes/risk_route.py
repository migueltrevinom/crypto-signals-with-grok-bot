"""Risk profile routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Risk.controllers import risk_controller

router = APIRouter(
    prefix="/risk-profiles",
    tags=["risk"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="Default risk seed. Not stored.")
async def list_risk_profiles() -> dict:
    return await risk_controller.list_profiles()
