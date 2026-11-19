"""Signup flag. Tokens are not issued in this pass."""

from typing import Any

from Core.config import get_settings
from Core.planning_seeds import TENANCY


async def show_config(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    settings = get_settings()
    return {
        "mode": "single_tenant" if not settings.public_signup else "public",
        "public_signup": settings.public_signup,
        "default_role_on_signup": TENANCY["default_role_on_signup"],
        "jwt_configured": bool(settings.jwt_secret),
    }
