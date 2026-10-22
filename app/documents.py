"""Beanie models the API and worker will register. Reserved models stay off this list."""

from Repositories.Alerts.models.alert_channel_model import AlertChannel
from Repositories.Alerts.models.alert_model import Alert
from Repositories.Backtests.models.backtest_event_model import BacktestEvent
from Repositories.Backtests.models.backtest_model import Backtest
from Repositories.Exchanges.models.exchange_source_model import ExchangeSource
from Repositories.MarketData.models.candle_model import Candle
from Repositories.Signals.models.scan_run_model import ScanRun
from Repositories.Signals.models.signal_model import Signal
from Repositories.Strategies.TimeMode.models.strategy_config_model import StrategyConfig
from Repositories.Watchlists.models.watchlist_model import Watchlist

DOCUMENT_MODELS = [
    Signal,
    ScanRun,
    Watchlist,
    StrategyConfig,
    Candle,
    ExchangeSource,
    AlertChannel,
    Alert,
    Backtest,
    BacktestEvent,
]
