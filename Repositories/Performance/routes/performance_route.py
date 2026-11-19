"""Authenticated track record. Empty until the house account runs forward."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Performance.controllers import performance_controller

router = APIRouter(
    prefix="/performance",
    tags=["performance"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/track-record", summary="Forward track record. Empty. Includes the disclaimer.")
async def track_record() -> dict:
    return await performance_controller.track_record()
