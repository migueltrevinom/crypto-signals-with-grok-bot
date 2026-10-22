"""Plan checks. Not wired to routes in this pass.

When a subscriber route is built, the dependency calls `require_entitlement`
after auth. Owner and admin bypass. A miss is 403 `entitlement_required`
plus an audit row. See docs/saas.md.
"""

from Core.errors import AppError


async def require_entitlement(code: str, entitlements: dict | None = None) -> None:
    del code, entitlements
    raise AppError(
        "Entitlement checks are not enforced yet",
        status_code=501,
        code="not_implemented",
    )
