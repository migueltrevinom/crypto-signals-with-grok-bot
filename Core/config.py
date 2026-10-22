"""Environment settings. Strategy parameters are not settings; they live in Mongo."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "crypto-signals-with-grok-bot"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_key: str = ""
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "crypto_signals"
    scan_interval_seconds: int = 900
    public_signup: bool = False
    jwt_secret: str = ""
    secrets_key: str = ""

    @property
    def api_key_required(self) -> bool:
        """Staging and production always require a key. Development requires one only if set."""
        if self.app_env != "development":
            return True
        return bool(self.api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
