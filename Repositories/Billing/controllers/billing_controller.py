"""Billing controller."""

from Repositories.Billing.modules import billing_module


async def list_plans() -> dict:
    data = await billing_module.list_plans(auth_user=None)
    return {"data": data, "total": len(data), "limit": 20, "page": 1, "pages": 1}
