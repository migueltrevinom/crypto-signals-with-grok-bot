"""Public compliance gate. Not an API-key route, and not legal advice."""

from fastapi import APIRouter

from Repositories.Compliance.controllers import compliance_controller

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/gate", summary="Lawyer-review gate. legal_advice is false.")
async def show_gate() -> dict:
    return await compliance_controller.show_gate()
