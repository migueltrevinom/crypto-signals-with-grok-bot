"""Motor client. The planning skeleton never calls connect()."""

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from Core.config import get_settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient | None:
    return _client


def get_database() -> AsyncIOMotorDatabase | None:
    if _client is None:
        return None
    return _client[get_settings().mongodb_db]


async def connect(models: list[type[Any]] | None = None) -> None:
    """Open Mongo and, when models are passed, init Beanie.

    Phase 1 calls this from the API lifespan and the worker. Not called now,
    so /health works with no database. `models` is the list from app.documents.
    """
    global _client
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.mongodb_url)
    if models:
        from beanie import init_beanie

        await init_beanie(database=get_database(), document_models=models)


async def disconnect() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
