"""Public performance page. No API key. Does not claim a record."""

from fastapi import APIRouter

from Repositories.Performance.controllers import performance_controller

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/performance", summary="Public performance placeholder and disclaimer.")
async def public_performance() -> dict:
    return await performance_controller.track_record()
