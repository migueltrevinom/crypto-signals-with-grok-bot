"""Watchlist routes. Thin: auth dependency, validation, controller."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Watchlists.controllers import watchlist_controller
from Repositories.Watchlists.middlewares.watchlist_middleware import WatchlistListQuery

router = APIRouter(
    prefix="/watchlists",
    tags=["watchlists"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List watchlists. Planning skeleton: empty page, no Mongo read.")
async def list_watchlists(params: WatchlistListQuery = Depends()) -> dict:
    return await watchlist_controller.get(params)
