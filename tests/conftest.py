"""Keep tests on development settings even if the shell has a key set."""

import pytest

from Core.config import get_settings


@pytest.fixture(autouse=True)
def development_settings(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("API_KEY", "")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
