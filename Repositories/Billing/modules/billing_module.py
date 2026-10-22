"""Plan seed. Checkout is not implemented."""

from typing import Any

from Core.planning_seeds import PLAN_SEEDS


async def list_plans(auth_user: dict | None = None) -> list[dict[str, Any]]:
    del auth_user
    return [{**plan, "persisted": False} for plan in PLAN_SEEDS]
