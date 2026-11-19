"""Resolved planning defaults. Mongo is the runtime store once phase 2 seeds it.

These values are Miguel's answers, not the old prototype ladder. `prototype/config.json`
stays untouched as the detection oracle for rules he has not replaced.
Controllers may read this module. Domain modules may read it. They do not
import each other.
"""

from typing import Any

LADDER_TIMEFRAMES = ["4h", "6h", "8h", "1d", "3d", "1w", "1M"]
SMA_FILTER_TIMEFRAME = "6h"
SMA_LENGTH = 70
DECISION_TIMEFRAMES = ["1w", "3d", "1d"]
ENTRY_TIMEFRAMES = ["4h", "6h", "8h"]
CONTEXT_TIMEFRAME = "1M"
PREFERRED_QUOTE_ASSETS = ["USDT"]

# Native ladder intervals checked against public docs on 2026-10-22.
# Resample targets use the named lower timeframe, aligned to Binance's grid.
# See docs/repositories.md (MarketData).
EXCHANGE_CATALOG: list[dict[str, Any]] = [
    {
        "name": "binance",
        "priority": 1,
        "kind": "spot_klines",
        "base_url": "https://api.binance.com",
        "market": "spot",
        "enabled": True,
        "auth": "none",
        "symbol_style": "concat",
        "native_timeframes": ["4h", "6h", "8h", "1d", "3d", "1w", "1M"],
        "resample_from": {},
    },
    {
        "name": "binance_vision",
        "priority": 2,
        "kind": "spot_klines",
        "base_url": "https://data-api.binance.vision",
        "market": "spot",
        "enabled": True,
        "auth": "none",
        "symbol_style": "concat",
        "native_timeframes": ["4h", "6h", "8h", "1d", "3d", "1w", "1M"],
        "resample_from": {},
    },
    {
        "name": "bybit",
        "priority": 3,
        "kind": "spot_klines",
        "base_url": "https://api.bybit.com",
        "market": "spot",
        "enabled": True,
        "auth": "none",
        "symbol_style": "concat",
        "native_timeframes": ["4h", "6h", "1d", "1w", "1M"],
        "resample_from": {"8h": "4h", "3d": "1d"},
    },
    {
        "name": "okx",
        "priority": 4,
        "kind": "spot_klines",
        "base_url": "https://www.okx.com",
        "market": "spot",
        "enabled": True,
        "auth": "none",
        "symbol_style": "dash",
        "native_timeframes": ["4h", "6h", "1d", "3d", "1w", "1M"],
        "resample_from": {"8h": "4h"},
    },
    {
        "name": "coinbase",
        "priority": 5,
        "kind": "spot_klines",
        "base_url": "https://api.exchange.coinbase.com",
        "market": "spot",
        "enabled": False,
        "auth": "none",
        "symbol_style": "dash",
        "native_timeframes": ["6h", "1d"],
        "resample_from": {"4h": "1h", "8h": "1h", "3d": "1d", "1w": "1d", "1M": "1d"},
    },
    {
        "name": "kraken",
        "priority": 6,
        "kind": "spot_klines",
        "base_url": "https://api.kraken.com",
        "market": "spot",
        "enabled": False,
        "auth": "none",
        "symbol_style": "alias",
        "native_timeframes": ["4h", "1d", "1w"],
        "resample_from": {"6h": "1h", "8h": "4h", "3d": "1d", "1M": "1d"},
    },
]

DEX_CATALOG: list[dict[str, Any]] = [
    {
        "name": "uniswap_v3",
        "kind": "dex_pool",
        "chain": "ethereum",
        "enabled": False,
        "quote_method": "pool_mid",
        "notes": "Planned connector. No orders.",
    },
    {
        "name": "dex_aggregator",
        "kind": "dex_aggregator",
        "chain": "ethereum",
        "enabled": False,
        "quote_method": "aggregator_quote",
        "notes": "Slot for an aggregator quote (OKX onchain or 0x). No orders.",
    },
]

CONFLUENCE_SEED: dict[str, Any] = {
    "id": None,
    "key": "time_mode_confluence",
    "version": 0,
    "active": True,
    "persisted": False,
    "decision_timeframes": DECISION_TIMEFRAMES,
    "entry_timeframes": ENTRY_TIMEFRAMES,
    "require_sma_6h": True,
    "weights": {
        "mode_confirmed": {"1M": 1, "1w": 3, "3d": 2, "1d": 2, "8h": 1, "6h": 1, "4h": 1},
        "block_break": {"1M": 1, "1w": 3, "3d": 2, "1d": 2, "8h": 1, "6h": 1, "4h": 1},
        "sma_6h_agreement": 2,
        "timeframe_in_control_agreement": 2,
        "htf_conflict_penalty": 3,
    },
    "thresholds": {"watch": 5, "entry": 8},
    "entry_timeframe_priority": ["4h", "6h", "8h"],
}

RISK_SEED: dict[str, Any] = {
    "id": None,
    "name": "default",
    "persisted": False,
    "user_id": None,
    "strategy_key": "time_mode",
    "symbol_id": None,
    "market": "any",
    "enabled": True,
    "risk_per_trade": {"mode": "percent_of_equity", "value": 0.01},
    "account": {
        "source": "manual",
        "venue": None,
        "manual_equity": None,
        "quote_asset": "USDT",
    },
    "max_leverage": 1,
    "max_notional_quote": None,
    "stop": {"method": "below_structure", "buffer_atr": 0.25},
    "trailing": {"enabled": True, "method": "expansion_candle"},
    "take_profit": {"method": "r_multiple", "targets": [2, 3]},
    "exit": {"rule": "two_lower_closes"},
}

TENANCY: dict[str, Any] = {
    "mode": "single_tenant",
    "public_signup": False,
    "default_role_on_signup": "free",
}

DISCLAIMER = (
    "Not investment advice. Simulated and historical results are not future results. "
    "This text is a product disclaimer, not a legal opinion."
)

# Prices are hypotheses in docs/competitive-analysis.md. price_cents stays null
# until Miguel sets a Stripe price. Entitlement keys match Stripe feature lookup keys.
PLAN_SEEDS: list[dict[str, Any]] = [
    {
        "code": "free",
        "name": "Free",
        "kind": "base",
        "public": True,
        "currency": "cad",
        "interval": "month",
        "price_cents": None,
        "price_hypothesis": "$0. Delayed BTC and ETH spot only.",
        "trial_days": 0,
        "grace_days": 0,
        "entitlements": {
            "signals.delay_seconds": 14400,
            "signals.max_pairs": 2,
            "signals.symbols": ["BTCUSDT", "ETHUSDT"],
            "signals.timeframes": ["1d", "1w"],
            "signals.markets": ["spot"],
            "channels": ["grok_chat"],
            "api.rate_limit_per_min": 0,
            "webhooks.max_endpoints": 0,
            "arbitrage.enabled": False,
            "history.days": 30,
            "backtests.per_month": 0,
            "paper_trading": True,
        },
    },
    {
        "code": "starter",
        "name": "Starter",
        "kind": "base",
        "public": True,
        "currency": "cad",
        "interval": "month",
        "price_cents": None,
        "price_hypothesis": "About $19–29/mo in the research. Not a price decision.",
        "trial_days": 7,
        "grace_days": 3,
        "entitlements": {
            "signals.delay_seconds": 0,
            "signals.max_pairs": 20,
            "signals.symbols": None,
            "signals.timeframes": ["1d", "3d", "1w"],
            "signals.markets": ["spot"],
            "channels": ["grok_chat", "email", "telegram"],
            "api.rate_limit_per_min": 0,
            "webhooks.max_endpoints": 0,
            "arbitrage.enabled": False,
            "history.days": 180,
            "backtests.per_month": 5,
            "paper_trading": True,
        },
    },
    {
        "code": "pro",
        "name": "Pro",
        "kind": "base",
        "public": True,
        "currency": "cad",
        "interval": "month",
        "price_cents": None,
        "price_hypothesis": "About $49–79/mo in the research. Not a price decision.",
        "trial_days": 14,
        "grace_days": 3,
        "entitlements": {
            "signals.delay_seconds": 0,
            "signals.max_pairs": None,
            "signals.symbols": None,
            "signals.timeframes": ["4h", "6h", "8h", "1d", "3d", "1w", "1M"],
            "signals.markets": ["spot", "futures"],
            "channels": ["grok_chat", "email", "telegram", "discord", "webhook"],
            "api.rate_limit_per_min": 60,
            "webhooks.max_endpoints": 3,
            "arbitrage.enabled": False,
            "history.days": None,
            "backtests.per_month": 50,
            "paper_trading": True,
        },
    },
    {
        "code": "arbitrage",
        "name": "Arbitrage",
        "kind": "addon",
        "attaches_to": ["starter", "pro"],
        "public": True,
        "currency": "cad",
        "interval": "month",
        "price_cents": None,
        "price_hypothesis": (
            "About $99+/mo in the research, anchored to ArbitrageScanner. Not a price decision."
        ),
        "trial_days": 0,
        "grace_days": 3,
        "entitlements": {
            "arbitrage.enabled": True,
            "signals.delay_seconds": 0,
            "channels": ["grok_chat", "telegram", "webhook"],
            "api.rate_limit_per_min": 120,
        },
    },
]

COMPLIANCE_GATE: dict[str, Any] = {
    "legal_advice": False,
    "lawyer_review_required": True,
    "public_signup_allowed": False,
    "references": [
        "CSA/CIRO Staff Notice 31-369",
        "NI 31-103 section 8.25",
    ],
    "rules_intended": [
        "same signal to every subscriber in a tier",
        "conflict disclosure with each signal",
        "no auto-trading and no copy-trading for payment",
        "futures signals geo-gated for Canada",
    ],
    "open_with_counsel": [
        "whether a per-user stop and size calculator is tailored advice",
    ],
}

ARBITRAGE_SETTINGS: dict[str, Any] = {
    "persisted": False,
    "min_net_spread_bps": 0,
    "default_slippage_bps": 5,
    "path_kinds": ["cross_exchange_spot", "cex_dex"],
    "place_orders": False,
}
