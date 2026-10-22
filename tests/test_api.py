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


def test_time_mode_defaults_match_prototype() -> None:
    config = load_prototype_config()
    response = client.get("/api/v1/strategies/time-mode")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["persisted"] is False
    assert data["params"] == config["params"]
    assert data["symbols"] == config["symbols"]
    assert data["timeframes"] == config["timeframes"]
    assert data["scanner"]["ltf_map"] == config["ltf_map"]
    assert data["params"]["confirm_atr_mult"] == 0.7


def test_exchanges_follow_prototype_order() -> None:
    config = load_prototype_config()
    response = client.get("/api/v1/exchanges")
    assert response.status_code == 200
    names = [row["name"] for row in response.json()["data"]]
    assert names == config["data_sources"]
    assert response.json()["data"][0]["base_url"] == "https://api.binance.com"
    assert response.json()["data"][0]["auth"] == "none"


def test_models_are_loaded_and_reserved_ones_are_not_registered() -> None:
    from Repositories.Arbitrage.models.arbitrage_opportunity_model import (
        ArbitrageOpportunity,
    )
    from Repositories.Futures.Positions.models.position_model import Position

    with TestClient(app):
        names = {model.Settings.name for model in app.state.document_models}
    assert "signals" in names
    assert "strategy_configs" in names
    assert "positions" not in names
    assert "arbitrage_opportunities" not in names
    assert Position.Settings.name == "positions"
    assert ArbitrageOpportunity.Settings.name == "arbitrage_opportunities"


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
