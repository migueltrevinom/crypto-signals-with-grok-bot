"""Default risk profile seed. Sizing is specified and not implemented."""

from typing import Any

from Core.planning_seeds import RISK_SEED


async def list_profiles(auth_user: dict | None = None) -> list[dict[str, Any]]:
    del auth_user
    return [dict(RISK_SEED)]
