"""Audit controller."""

from Core.http import list_response
from Repositories.Audit.middlewares.audit_middleware import AuditListQuery
from Repositories.Audit.modules import audit_module


async def get(params: AuditListQuery) -> dict:
    data = await audit_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
