"""Skeleton routes: health, empty pages, prototype-backed reads, and the API key."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from Core.config import get_settings
from Core.prototype_config import load_prototype_config

client = TestClient(app)

EMPTY_PAGES = [
    "/api/v1/signals",
    "/api/v1/watchlists",
    "/api/v1/backtests",
    "/api/v1/alerts",
    "/api/v1/alert-channels",
    "/api/v1/market-data/candles",
    "/api/v1/symbols",
    "/api/v1/users",
    "/api/v1/positions",
    "/api/v1/position-events",
    "/api/v1/entry-plans",
    "/api/v1/arbitrage/opportunities",
]


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "crypto-signals-with-grok-bot"
    assert body["environment"] == "development"
    assert body["mongo"] == "not_connected"
    assert body["scanner"] == "not_ported"


def test_unknown_path_is_404() -> None:
    response = client.get("/nope")
    assert response.status_code == 404


def test_empty_pages() -> None:
    for path in EMPTY_PAGES:
        response = client.get(path)
        assert response.status_code == 200, path
        assert response.json() == {
            "data": [],
            "total": 0,
            "limit": 20,
            "page": 1,
            "pages": 0,
        }


def test_page_query_is_validated() -> None:
    response = client.get("/api/v1/signals", params={"page": 0})
    assert response.status_code == 422


def test_scanner_status() -> None:
    response = client.get("/api/v1/scanner/status")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "not_ported"
    assert response.json()["data"]["last_run"] is None


def test_time_mode_uses_resolved_sma_and_ladder() -> None:
    config = load_prototype_config()
    response = client.get("/api/v1/strategies/time-mode")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["persisted"] is False
    assert data["params"]["confirm_atr_mult"] == config["params"]["confirm_atr_mult"]
    assert data["params"]["sma_filter_timeframe"] == "6h"
    assert data["ladder"]["timeframes"] == ["4h", "6h", "8h", "1d", "3d", "1w", "1M"]
    assert "ltf_map" not in data["scanner"]
    assert config["ltf_map"]["1h"] == "15m"
    assert config["params"]["sma_filter_timeframe"] == "entry"


def test_ladder_settings_seed() -> None:
    response = client.get("/api/v1/settings/ladder")
    assert response.status_code == 200
    value = response.json()["data"]["value"]
    assert value["sma_filter_timeframe"] == "6h"
    assert value["timeframes"][0] == "4h"
    assert value["timeframes"][-1] == "1M"
    assert value["alignment"] == "binance"


def test_exchanges_catalog_and_symbol_style() -> None:
    response = client.get("/api/v1/exchanges")
    assert response.status_code == 200
    rows = {row["name"]: row for row in response.json()["data"]}
    assert rows["binance"]["base_url"] == "https://api.binance.com"
    assert "8h" in rows["binance"]["native_timeframes"]
    assert rows["bybit"]["resample_from"]["8h"] == "4h"
    assert "3d" in rows["bybit"]["resample_from"]
    assert rows["okx"]["symbol_style"] == "dash"
    assert rows["okx"]["resample_from"]["8h"] == "4h"
    assert rows["kraken"]["symbol_style"] == "alias"
    assert rows["coinbase"]["enabled"] is False


def test_confluence_and_risk_seeds() -> None:
    confluence = client.get("/api/v1/strategies/confluence")
    assert confluence.status_code == 200
    body = confluence.json()["data"]
    assert body["require_sma_6h"] is True
    assert body["thresholds"]["entry"] == 8
    assert body["decision_timeframes"] == ["1w", "3d", "1d"]
    risk = client.get("/api/v1/risk-profiles")
    assert risk.status_code == 200
    profile = risk.json()["data"][0]
    assert profile["persisted"] is False
    assert profile["stop"]["method"] == "below_structure"
    assert profile["risk_per_trade"]["value"] == 0.01
    assert profile["account"]["manual_equity"] is None


def test_alert_feed_is_empty() -> None:
    response = client.get("/api/v1/alerts/feed")
    assert response.status_code == 200
    assert response.json() == {"data": [], "cursor": None, "limit": 50}


def test_arbitrage_settings_do_not_place_orders() -> None:
    response = client.get("/api/v1/settings/arbitrage")
    assert response.status_code == 200
    assert response.json()["data"]["value"]["place_orders"] is False


def test_models_include_positions_and_arbitrage() -> None:
    with TestClient(app):
        names = {model.Settings.name for model in app.state.document_models}
    assert "signals" in names
    assert "symbols" in names
    assert "risk_profiles" in names
    assert "positions" in names
    assert "arbitrage_opportunities" in names
    assert "confluence_configs" in names


def test_production_requires_a_configured_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("API_KEY", "")
    get_settings.cache_clear()
    response = client.get("/api/v1/signals")
    assert response.status_code == 500
    assert response.json()["code"] == "server_misconfigured"
    health = client.get("/health")
    assert health.status_code == 200


def test_production_rejects_a_bad_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("API_KEY", "secret-value")
    get_settings.cache_clear()
    missing = client.get("/api/v1/signals")
    assert missing.status_code == 401
    assert missing.json() == {"message": "Unauthorized", "code": "unauthorized"}
    ok = client.get("/api/v1/signals", headers={"X-API-Key": "secret-value"})
    assert ok.status_code == 200
