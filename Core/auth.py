"""Single shared API key. There is no user collection in this plan."""

from fastapi import Header

from Core.config import get_settings
from Core.errors import AppError


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.api_key_required:
        return
    if not settings.api_key:
        raise AppError(
            "API_KEY is not configured",
            status_code=500,
            code="server_misconfigured",
        )
    if x_api_key != settings.api_key:
        raise AppError("Unauthorized", status_code=401, code="unauthorized")
