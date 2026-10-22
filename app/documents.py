"""Beanie models the API and worker will register when Mongo connects.

connect() is not called in this planning skeleton. The list is the schema.
"""

from Repositories.Alerts.models.alert_channel_model import AlertChannel
from Repositories.Alerts.models.alert_model import Alert
from Repositories.Arbitrage.models.arbitrage_opportunity_model import ArbitrageOpportunity
from Repositories.Arbitrage.models.venue_quote_model import VenueQuote
from Repositories.Audit.models.audit_log_model import AuditLog
from Repositories.Auth.models.api_key_model import ApiKey
from Repositories.Auth.models.refresh_token_model import RefreshToken
from Repositories.Backtests.models.backtest_event_model import BacktestEvent
from Repositories.Backtests.models.backtest_model import Backtest
from Repositories.Billing.models.payment_event_model import PaymentEvent
from Repositories.Billing.models.plan_model import Plan
from Repositories.Billing.models.subscription_model import Subscription
from Repositories.Dexes.models.dex_venue_model import DexVenue
from Repositories.ExchangeAccounts.models.exchange_account_model import ExchangeAccount
from Repositories.Exchanges.models.exchange_source_model import ExchangeSource
from Repositories.MarketData.models.candle_model import Candle
from Repositories.PaperTrading.models.paper_account_model import PaperAccount
from Repositories.PaperTrading.models.paper_fill_model import PaperFill
from Repositories.Performance.models.outcome_model import Outcome
from Repositories.Performance.models.signal_log_model import SignalLog
from Repositories.Positions.models.position_event_model import PositionEvent
from Repositories.Positions.models.position_model import Position
from Repositories.Publications.models.publication_model import Publication
from Repositories.Risk.models.risk_profile_model import RiskProfile
from Repositories.Settings.models.app_setting_model import AppSetting
from Repositories.Signals.models.scan_run_model import ScanRun
from Repositories.Signals.models.signal_model import Signal
from Repositories.Strategies.Confluence.models.confluence_config_model import ConfluenceConfig
from Repositories.Strategies.Confluence.models.entry_plan_model import EntryPlan
from Repositories.Strategies.TimeMode.models.strategy_config_model import StrategyConfig
from Repositories.Symbols.models.symbol_model import Symbol
from Repositories.Users.models.user_model import User
from Repositories.Watchlists.models.watchlist_model import Watchlist

DOCUMENT_MODELS = [
    User,
    ApiKey,
    RefreshToken,
    Plan,
    Subscription,
    PaymentEvent,
    Publication,
    SignalLog,
    Outcome,
    PaperAccount,
    PaperFill,
    ExchangeAccount,
    AuditLog,
    Symbol,
    AppSetting,
    ExchangeSource,
    DexVenue,
    Candle,
    StrategyConfig,
    ConfluenceConfig,
    EntryPlan,
    Signal,
    ScanRun,
    Watchlist,
    RiskProfile,
    Position,
    PositionEvent,
    AlertChannel,
    Alert,
    Backtest,
    BacktestEvent,
    ArbitrageOpportunity,
    VenueQuote,
]
