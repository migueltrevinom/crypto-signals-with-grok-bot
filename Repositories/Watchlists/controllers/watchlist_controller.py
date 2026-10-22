"""Watchlist controller. Calls the module and shapes the list envelope."""

from Core.http import list_response
from Repositories.Watchlists.middlewares.watchlist_middleware import WatchlistListQuery
from Repositories.Watchlists.modules import watchlist_module


async def get(params: WatchlistListQuery) -> dict:
    data = await watchlist_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
