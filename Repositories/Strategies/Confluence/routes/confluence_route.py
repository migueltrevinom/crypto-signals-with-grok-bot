"""Confluence routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Strategies.Confluence.controllers import confluence_controller
from Repositories.Strategies.Confluence.middlewares.confluence_middleware import (
    EntryPlanListQuery,
)

router = APIRouter(tags=["confluence"], dependencies=[Depends(require_api_key)])


@router.get(
    "/strategies/confluence",
    summary="Confluence weight seed. Not stored.",
)
async def show_confluence() -> dict:
    return await confluence_controller.show_config()


@router.get("/entry-plans", summary="Entry plans. Planning skeleton: empty page.")
async def list_entry_plans(params: EntryPlanListQuery = Depends()) -> dict:
    return await confluence_controller.list_entry_plans(params.model_dump())
