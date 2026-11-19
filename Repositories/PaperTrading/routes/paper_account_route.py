"""PaperAccount routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.PaperTrading.controllers import paper_account_controller
from Repositories.PaperTrading.middlewares.paper_account_middleware import PaperAccountListQuery

router = APIRouter(
    prefix="/paper/accounts",
    tags=["paper"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List paper accounts. Empty. No house account yet.")
async def list_paper_accounts(params: PaperAccountListQuery = Depends()) -> dict:
    return await paper_account_controller.get(params)
