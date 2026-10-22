"""Deployment key today. JWT and user API keys are specified in docs/saas.md.

`require_api_key` stays the check on current routes so an empty key in
development still opens the API. `require_user` will verify a JWT or a
hashed user key. Until that code exists it delegates here, which keeps
single-tenant mode working.
"""

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


async def require_user(x_api_key: str | None = Header(default=None)) -> None:
    """Future JWT-or-user-key dependency. Delegates to the deployment key for now."""
    await require_api_key(x_api_key)
