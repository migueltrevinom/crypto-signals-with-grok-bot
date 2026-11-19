"""Domain errors use {message, code} and do not leak unexpected exception text."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from Core.errors import AppError, register_exception_handlers


def test_app_error_shape() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/missing")
    async def missing() -> None:
        raise AppError("Signal not found", status_code=404, code="not_found")

    response = TestClient(app).get("/missing")
    assert response.status_code == 404
    assert response.json() == {"message": "Signal not found", "code": "not_found"}


def test_unexpected_error_is_generic() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("disk path /secret")

    response = TestClient(app, raise_server_exceptions=False).get("/boom")
    assert response.status_code == 500
    assert response.json() == {
        "message": "Internal server error",
        "code": "internal_error",
    }
    assert "secret" not in response.text
