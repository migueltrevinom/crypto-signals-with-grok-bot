"""Compliance controller."""

from Repositories.Compliance.modules import compliance_module


async def show_gate() -> dict:
    return {"data": await compliance_module.show_gate(auth_user=None)}
