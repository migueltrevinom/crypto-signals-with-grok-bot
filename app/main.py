"""FastAPI entrypoint. Does not connect to Mongo in this planning skeleton."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app.documents import DOCUMENT_MODELS
from app.router import api_router
from Core.config import get_settings
from Core.errors import register_exception_handlers
from Core.logging import configure_logging


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    mongo: str
    scanner: str


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_logging(get_settings().log_level)
    # Document classes are imported so a broken model fails at startup.
    # connect() is intentionally not called. See Core.database.
    _app.state.document_models = DOCUMENT_MODELS
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    register_exception_handlers(app)
    app.state.document_models = DOCUMENT_MODELS
    app.include_router(api_router)

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health() -> HealthResponse:
        current = get_settings()
        return HealthResponse(
            status="ok",
            service=current.app_name,
            environment=current.app_env,
            mongo="not_connected",
            scanner="not_ported",
        )

    return app


app = create_app()


def main() -> None:
    import uvicorn

    settings = get_settings()
    configure_logging(settings.log_level)
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
