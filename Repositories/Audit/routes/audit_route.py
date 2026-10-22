"""Audit routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Audit.controllers import audit_controller
from Repositories.Audit.middlewares.audit_middleware import AuditListQuery

router = APIRouter(
    prefix="/audit-logs",
    tags=["audit"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List audit logs. Empty.")
async def list_audit_logs(params: AuditListQuery = Depends()) -> dict:
    return await audit_controller.get(params)
