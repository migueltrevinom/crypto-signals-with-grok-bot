"""Mounts domain routers under /api/v1."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Core.config import get_settings
from Repositories.Alerts.routes.alert_channel_route import router as alert_channel_router
from Repositories.Alerts.routes.alert_route import router as alert_router
from Repositories.Backtests.routes.backtest_route import router as backtest_router
from Repositories.Exchanges.routes.exchange_route import router as exchange_router
from Repositories.MarketData.routes.candle_route import router as candle_router
from Repositories.Signals.routes.signal_route import router as signal_router
from Repositories.Strategies.TimeMode.routes.timemode_route import router as timemode_router
from Repositories.Watchlists.routes.watchlist_route import router as watchlist_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(signal_router)
api_router.include_router(watchlist_router)
api_router.include_router(backtest_router)
api_router.include_router(alert_router)
api_router.include_router(alert_channel_router)
api_router.include_router(candle_router)
api_router.include_router(exchange_router)
api_router.include_router(timemode_router)


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
