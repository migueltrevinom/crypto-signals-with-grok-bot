"""Mounts domain routers under /api/v1."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Core.config import get_settings
from Repositories.Alerts.routes.alert_channel_route import router as alert_channel_router
from Repositories.Alerts.routes.alert_feed_route import router as alert_feed_router
from Repositories.Alerts.routes.alert_route import router as alert_router
from Repositories.Arbitrage.routes.arbitrage_route import router as arbitrage_router
from Repositories.Backtests.routes.backtest_route import router as backtest_router
from Repositories.Dexes.routes.dex_route import router as dex_router
from Repositories.Exchanges.routes.exchange_route import router as exchange_router
from Repositories.MarketData.routes.candle_route import router as candle_router
from Repositories.Positions.routes.position_event_route import router as position_event_router
from Repositories.Positions.routes.position_route import router as position_router
from Repositories.Risk.routes.risk_route import router as risk_router
from Repositories.Settings.routes.settings_route import router as settings_router
from Repositories.Signals.routes.signal_route import router as signal_router
from Repositories.Strategies.Confluence.routes.confluence_route import router as confluence_router
from Repositories.Strategies.TimeMode.routes.timemode_route import router as timemode_router
from Repositories.Symbols.routes.symbol_route import router as symbol_router
from Repositories.Users.routes.user_route import router as user_router
from Repositories.Watchlists.routes.watchlist_route import router as watchlist_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(signal_router)
api_router.include_router(watchlist_router)
api_router.include_router(backtest_router)
api_router.include_router(alert_router)
api_router.include_router(alert_feed_router)
api_router.include_router(alert_channel_router)
api_router.include_router(candle_router)
api_router.include_router(exchange_router)
api_router.include_router(dex_router)
api_router.include_router(timemode_router)
api_router.include_router(confluence_router)
api_router.include_router(settings_router)
api_router.include_router(symbol_router)
api_router.include_router(user_router)
api_router.include_router(risk_router)
api_router.include_router(position_router)
api_router.include_router(position_event_router)
api_router.include_router(arbitrage_router)


@api_router.get(
    "/scanner/status",
    tags=["scanner"],
    summary="Scanner placeholder. Detection is not ported.",
    dependencies=[Depends(require_api_key)],
)
async def scanner_status() -> dict:
    settings = get_settings()
    return {
        "data": {
            "status": "not_ported",
            "interval_seconds": settings.scan_interval_seconds,
            "last_run": None,
        }
    }
